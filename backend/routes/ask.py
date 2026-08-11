from fastapi import APIRouter, HTTPException
from models.query import QueryRequest, AskResponse, PlayerListResponse, PlayerDetailResponse
import logging, time, psutil, asyncio
from typing import Optional, List, Dict
from config import Config

from services.gemini import (
    generate_answer, 
    classify_fields, 
    build_context_by_player, 
    extract_years_from_query, 
    identify_primary_stat, 
    is_superlative_query,
    analyze_query_intent
)
from services.player_store import player_store

import re

def safe_float(val) -> float:
    if not val:
        return 0.0
    try:
        cleaned = re.sub(r"[^\d.]", "", str(val))
        return float(cleaned) if cleaned else 0.0
    except (ValueError, TypeError):
        return 0.0

logger = logging.getLogger(__name__)
ask_router = APIRouter()

# 💓 Heartbeat logger for long background requests
async def heartbeat():
    while True:
        await asyncio.sleep(5)
        logger.info("💓 Backend actively processing request...")

# Lazy Pinecone index initialization
_pinecone_index = None

def get_pinecone_index():
    global _pinecone_index
    if _pinecone_index is None:
        from pinecone import Pinecone
        pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        _pinecone_index = pc.Index(Config.INDEX_NAME)
    return _pinecone_index


@ask_router.get("/ask")
async def ask_info():
    return {"message": "POST { 'query': '...', 'vector': [...] }"}


@ask_router.get("/players", response_model=PlayerListResponse)
async def get_all_players() -> PlayerListResponse:
    t1 = time.time()
    players = player_store.get_all_player_names()
    logger.info(f"⚡ Fetched {len(players)} player names in {(time.time() - t1)*1000:.2f}ms")
    return PlayerListResponse(total_players=len(players), players=players)


@ask_router.get("/players/{player_name}", response_model=PlayerDetailResponse)
async def get_player_by_name(player_name: str) -> PlayerDetailResponse:
    t1 = time.time()
    recs = player_store.get_player_records(player_name)
    if not recs:
        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found.")
    canonical_name = recs[0].get("Player_Name", player_name)
    logger.info(f"⚡ Direct lookup for '{canonical_name}' returned {len(recs)} records in {(time.time() - t1)*1000:.2f}ms")
    return PlayerDetailResponse(player_name=canonical_name, total_records=len(recs), records=recs)


@ask_router.post("/ask", response_model=AskResponse)
async def ask_query(payload: QueryRequest) -> AskResponse:
    start_time = time.time()
    query = payload.query.strip() if payload.query else ""
    vector = payload.vector

    logger.info(f"🟢 Query received: {query}")
    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        # 🧠 Step 1: Pre-Fetch AI Query Intent Analysis (Gemini AI as Deciding Factor)
        ai_intent = analyze_query_intent(query)
        logger.info(f"🤖 Gemini AI Router Decision: {ai_intent}")

        intent = ai_intent.get("query_intent", "general_semantic")
        detected_players = ai_intent.get("target_players", [])
        years = ai_intent.get("target_years", [])
        recommended_strategy = ai_intent.get("recommended_strategy", "vector_search")
        is_superlative = (intent == "superlative_ranking") or is_superlative_query(query)

        # Fallback entity extraction if Gemini missed them
        if not detected_players:
            detected_players = player_store.extract_players_from_query(query)
        if not years:
            years = extract_years_from_query(query)

        results: List[Dict] = []
        retrieval_method = "unknown"

        # OPTIMIZATION FETCHING FLOW (GUIDED BY GEMINI AI)
        # Option A: Direct Player Store Lookup (Guided by Gemini AI player/comparison decision)
        if (recommended_strategy == "direct_player_store" or detected_players) and player_store.is_loaded:
            t1 = time.time()
            retrieval_method = "direct_player_store_ai_guided"
            for p in detected_players:
                p_recs = player_store.get_player_records(p)
                if years:
                    p_recs = [r for r in p_recs if r.get("Year") in [str(y) for y in years]]
                results.extend(p_recs)
            logger.info(f"⚡ Gemini-Guided Direct player lookup fetched {len(results)} records in {(time.time() - t1)*1000:.2f}ms")

        # Option B: Superlative Ranking Lookup (Guided by Gemini AI ranking decision)
        elif (recommended_strategy == "superlative_store" or is_superlative) and player_store.is_loaded:
            t1 = time.time()
            retrieval_method = "superlative_player_store_ai_guided"
            if years:
                results = player_store.get_records_by_years(years)
            else:
                results = player_store.get_all_records()
            logger.info(f"⚡ Gemini-Guided Superlative in-memory lookup fetched {len(results)} records in {(time.time() - t1)*1000:.2f}ms")

        # Option C: Semantic fallback -> Use Pinecone vector search
        elif vector and len(vector) > 0:
            t1 = time.time()
            retrieval_method = "pinecone_vector_search"
            filter_dict = None
            if years:
                if len(years) == 1:
                    filter_dict = {"Year": {"$eq": str(years[0])}}
                else:
                    filter_dict = {"Year": {"$in": [str(y) for y in years]}}

            top_k = 200 if (is_superlative and filter_dict) else (50 if filter_dict else 100)
            index = get_pinecone_index()
            response = index.query(
                vector=vector, 
                top_k=top_k, 
                include_metadata=True,
                filter=filter_dict
            )
            raw_results = [match.metadata for match in response["matches"]]
            results = [r for r in raw_results if r]
            logger.info(f"🌐 Pinecone vector search fetched {len(results)} records in {time.time() - t1:.2f}s")

        # Option D: Fallback to all player store records if no vector provided
        elif player_store.is_loaded:
            retrieval_method = "fallback_all_store"
            if years:
                results = player_store.get_records_by_years(years)
            else:
                results = player_store.get_all_records()

        logger.info(f"📊 Total retrieved records: {len(results)} via [{retrieval_method}]")

        # 🧠 Step 4: Classify fields & identify primary stat for ranking
        relevant_fields = classify_fields(query)
        primary_stat = identify_primary_stat(query, relevant_fields)
        logger.info(f"🎯 Relevant fields: {relevant_fields}, Primary stat: {primary_stat}")

        # 🧠 Step 5: Sort results by primary stat if applicable
        if primary_stat and results:
            try:
                valid_results = [r for r in results if safe_float(r.get(primary_stat)) > 0]
                if valid_results:
                    results = sorted(valid_results, key=lambda r: safe_float(r.get(primary_stat)), reverse=True)
            except Exception as e:
                logger.warning(f"⚠️ Sorting by {primary_stat} failed: {e}")

        # 🧠 Step 6: Build focused context with adaptive limits
        players_for_context = detected_players if detected_players else None
        
        # Adaptive record limits per player:
        # - Specific player / comparison query: None (include ALL years of career)
        # - Superlative ranking query: 3 records per player
        # - Broad / no-player query: 2 records per player
        if players_for_context:
            max_records_per_player = None
        elif is_superlative:
            max_records_per_player = 3
        else:
            max_records_per_player = 2

        context = build_context_by_player(
            records=results,
            relevant_fields=relevant_fields,
            max_per_player=max_records_per_player,
            target_players=players_for_context,
            threshold=75
        )

        # ✨ Step 7: Generate answer via Gemini
        t3 = time.time()
        try:
            answer = generate_answer(query, context) if query else "Vector-only query"
        except Exception as e:
            answer = "⚠️ Answer generation failed. Please try again."
            logger.error(f"Gemini error: {e}")
        logger.info(f"⏱ Gemini answer generated in {time.time() - t3:.2f}s")

        mem_used = psutil.Process().memory_info().rss / 1024**2
        logger.info(f"🧠 Memory after query: {mem_used:.2f} MiB")
        logger.info(f"⏱ Total query response time: {time.time() - start_time:.2f}s")

        # 🧹 Strip zero / null / empty fields from returned results payload to clean up response
        cleaned_results = []
        for r in results:
            clean_r = {k: v for k, v in r.items() if v not in (None, "", "0", 0, "0.0")}
            if clean_r:
                cleaned_results.append(clean_r)

        # Adaptive response result capping:
        # - If specific players detected: return ALL clean records for those players
        # - If superlative: return top 30
        # - Default: return top 20
        if detected_players:
            final_results = cleaned_results
        elif is_superlative:
            final_results = cleaned_results[:30]
        else:
            final_results = cleaned_results[:20]

        return AskResponse(query=query, answer=answer, results=final_results)

    finally:
        heartbeat_task.cancel()
        try:
            await heartbeat_task
        except asyncio.CancelledError:
            pass
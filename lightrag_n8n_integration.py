#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LightRAG + N8N Integration - Production Ready Code Examples
==========================================================

Este archivo contiene ejemplos de código listos para usar en integración
de LightRAG con N8N. Todos los ejemplos incluyen manejo de errores,
logging y mejores prácticas de seguridad.

Autor: GitHub Copilot
Fecha: 2024
Versión: 1.0
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import re
from enum import Enum

# Configuración de logging sanitizado
class SanitizingFormatter(logging.Formatter):
    \"\"\"Formatter que sanitiza credenciales en logs\"\"\"
    SENSITIVE_PATTERNS = [
        (r'api[_-]?key[\"\\']?\\s*[:=]\\s*[\"\\']?([^\"\\\'\\s]+)', 'api_key'),
        (r'password[\"\\']?\\s*[:=]\\s*[\"\\']?([^\"\\\'\\s]+)', 'password'),
        (r'token[\"\\']?\\s*[:=]\\s*[\"\\']?([^\"\\\'\\s]+)', 'token'),
        (r'authorization[\"\\']?\\s*[:=]\\s*[\"\\']?([^\"\\\'\\s]+)', 'auth'),
    ]
    
    def format(self, record):
        msg = super().format(record)
        for pattern, field_type in self.SENSITIVE_PATTERNS:
            msg = re.sub(
                pattern,
                f'{field_type}=\"***\"',
                msg,
                flags=re.IGNORECASE
            )
        return msg

# Setup logger con sanitización
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = SanitizingFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# ============================================================================
# 1. CONFIGURATION MANAGEMENT
# ============================================================================

class ConfigError(Exception):
    \"\"\"Raised when configuration is invalid\"\"\"
    pass


@dataclass
class LightRAGConfig:
    \"\"\"Configuration for LightRAG\"\"\"
    api_url: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    
    @classmethod
    def from_env(cls) -> 'LightRAGConfig':
        \"\"\"Load configuration from environment variables\"\"\"
        api_url = os.getenv('LIGHTRAG_API_URL')
        api_key = os.getenv('LIGHTRAG_API_KEY')
        
        if not api_url or not api_key:
            raise ConfigError(
                'Missing required env vars: LIGHTRAG_API_URL, LIGHTRAG_API_KEY'
            )
        
        return cls(
            api_url=api_url,
            api_key=api_key,
            timeout=int(os.getenv('LIGHTRAG_TIMEOUT', '30')),
            max_retries=int(os.getenv('LIGHTRAG_MAX_RETRIES', '3')),
            retry_delay=float(os.getenv('LIGHTRAG_RETRY_DELAY', '1.0')),
        )
    
    def validate(self) -> None:
        \"\"\"Validate configuration\"\"\"
        if not self.api_url.startswith(('http://', 'https://')):
            raise ConfigError(f'Invalid API URL: {self.api_url}')
        if len(self.api_key) < 10:
            raise ConfigError('API key too short')
        if self.timeout <= 0:
            raise ConfigError('Timeout must be positive')


# ============================================================================
# 2. REQUEST HANDLING & RETRY LOGIC
# ============================================================================

class QueryMode(str, Enum):
    \"\"\"Query modes for LightRAG\"\"\"
    LOCAL = 'local'
    NAIVE = 'naive'
    GLOBAL = 'global'
    HYBRID = 'hybrid'


def retry_on_exception(max_retries: int = 3, delay: float = 1.0):
    \"\"\"Decorator for retry logic\"\"\"
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    logger.info(f'Attempt {attempt + 1}/{max_retries} for {func.__name__}')
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(
                            f'Attempt {attempt + 1} failed: {str(e)}. '
                            f'Retrying in {wait_time}s...'
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f'All {max_retries} attempts failed for {func.__name__}'
                        )
            raise last_exception
        return async_wrapper
    return decorator


# ============================================================================
# 3. LIGHTRAG CLIENT
# ============================================================================

class LightRAGClient:
    \"\"\"Production-ready client for LightRAG API\"\"\"
    
    def __init__(self, config: LightRAGConfig):
        self.config = config
        self.config.validate()
        self.session = None
        logger.info('LightRAGClient initialized')
    
    async def __aenter__(self):
        \"\"\"Async context manager entry\"\"\"
        import aiohttp
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        \"\"\"Async context manager exit\"\"\"
        if self.session:
            await self.session.close()
    
    def _get_headers(self) -> Dict[str, str]:
        \"\"\"Get HTTP headers with authorization\"\"\"
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.config.api_key}',
            'User-Agent': 'LightRAG-N8N-Integration/1.0',
        }
    
    @retry_on_exception(max_retries=3, delay=1.0)
    async def insert_documents(
        self,
        documents: List[str],
        doc_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        \"\"\"
        Insert documents into LightRAG knowledge graph.
        
        Args:
            documents: List of document texts
            doc_id: Optional document ID
            
        Returns:
            Response from LightRAG API
            
        Raises:
            ConfigError: If client not initialized
            Exception: If request fails
        \"\"\"
        if not self.session:
            raise ConfigError('Client not initialized. Use async context manager.')
        
        if not documents:
            raise ValueError('Documents list cannot be empty')
        
        if any(not doc.strip() for doc in documents):
            raise ValueError('Empty documents not allowed')
        
        payload = {
            'documents': documents,
        }
        
        if doc_id:
            payload['doc_id'] = doc_id
        
        logger.info(f'Inserting {len(documents)} document(s) with ID: {doc_id}')
        
        async with self.session.post(
            f'{self.config.api_url}/api/documents',
            json=payload,
            headers=self._get_headers(),
            timeout=self.config.timeout,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f'Insert failed with status {response.status}: {error_text}')
                raise Exception(f'Insert failed: {response.status}')
            
            result = await response.json()
            logger.info(f'Successfully inserted documents: {result}')
            return result
    
    @retry_on_exception(max_retries=3, delay=1.0)
    async def query(
        self,
        prompt: str,
        mode: QueryMode = QueryMode.HYBRID,
        top_k: int = 10,
        similarity_threshold: float = 0.5,
    ) -> Dict[str, Any]:
        \"\"\"
        Query the knowledge graph using LightRAG.
        
        Args:
            prompt: Query text
            mode: Query mode (local, naive, global, hybrid)
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            Query results with response and references
            
        Raises:
            ValueError: If inputs are invalid
            Exception: If request fails
        \"\"\"
        if not self.session:
            raise ConfigError('Client not initialized. Use async context manager.')
        
        if not prompt or not prompt.strip():
            raise ValueError('Prompt cannot be empty')
        
        if not 1 <= top_k <= 100:
            raise ValueError('top_k must be between 1 and 100')
        
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError('similarity_threshold must be between 0.0 and 1.0')
        
        payload = {
            'prompt': prompt,
            'param': {
                'mode': mode.value,
                'top_k': top_k,
                'similarity_threshold': similarity_threshold,
            }
        }
        
        logger.info(f'Querying with mode={mode.value}, top_k={top_k}')
        
        async with self.session.post(
            f'{self.config.api_url}/api/query',
            json=payload,
            headers=self._get_headers(),
            timeout=self.config.timeout,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f'Query failed with status {response.status}: {error_text}')
                raise Exception(f'Query failed: {response.status}')
            
            result = await response.json()
            logger.info(f'Query returned {len(result.get("references", []))} references')
            return result
    
    async def delete_document(self, doc_id: str) -> Dict[str, Any]:
        \"\"\"
        Delete a document from the knowledge graph.
        
        Args:
            doc_id: Document ID to delete
            
        Returns:
            Deletion result
        \"\"\"
        if not self.session:
            raise ConfigError('Client not initialized. Use async context manager.')
        
        if not doc_id or not doc_id.strip():
            raise ValueError('doc_id cannot be empty')
        
        logger.info(f'Deleting document: {doc_id}')
        
        async with self.session.delete(
            f'{self.config.api_url}/api/documents/{doc_id}',
            headers=self._get_headers(),
            timeout=self.config.timeout,
        ) as response:
            if response.status not in [200, 204]:
                error_text = await response.text()
                logger.error(f'Delete failed with status {response.status}: {error_text}')
                raise Exception(f'Delete failed: {response.status}')
            
            result = await response.json() if response.status == 200 else {'deleted': True}
            logger.info(f'Document deleted successfully')
            return result


# ============================================================================
# 4. N8N INTEGRATION FUNCTIONS
# ============================================================================

async def n8n_insert_document(data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    N8N integration function for inserting documents.
    
    Expected input:
    {
        'documents': ['doc1', 'doc2'],
        'doc_id': 'optional_id'
    }
    \"\"\"
    try:
        config = LightRAGConfig.from_env()
        
        async with LightRAGClient(config) as client:
            result = await client.insert_documents(
                documents=data.get('documents', []),
                doc_id=data.get('doc_id'),
            )
        
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat(),
        }
    
    except Exception as e:
        logger.error(f'Insert operation failed: {str(e)}')
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
        }


async def n8n_query(data: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    N8N integration function for querying.
    
    Expected input:
    {
        'question': 'Your question',
        'mode': 'hybrid',  # optional
        'top_k': 10,       # optional
    }
    \"\"\"
    try:
        config = LightRAGConfig.from_env()
        
        # Validate input
        question = data.get('question', '').strip()
        if not question:
            raise ValueError('question field is required')
        
        mode = QueryMode(data.get('mode', 'hybrid'))
        top_k = int(data.get('top_k', 10))
        
        async with LightRAGClient(config) as client:
            result = await client.query(
                prompt=question,
                mode=mode,
                top_k=top_k,
                similarity_threshold=data.get('similarity_threshold', 0.5),
            )
        
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat(),
        }
    
    except ValueError as e:
        logger.error(f'Invalid input: {str(e)}')
        return {
            'success': False,
            'error': f'Invalid input: {str(e)}',
            'timestamp': datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f'Query operation failed: {str(e)}')
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
        }


# ============================================================================
# 5. BATCH PROCESSING
# ============================================================================

class DocumentBatch:
    \"\"\"Handle batch processing of documents\"\"\"
    
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.docs: List[str] = []
        self.created_at = datetime.now()
    
    def add(self, document: str) -> bool:
        \"\"\"Add document to batch. Returns True if batch is full.\"\"\"
        if len(document.strip()) == 0:
            logger.warning('Skipping empty document')
            return False
        
        self.docs.append(document)
        return len(self.docs) >= self.batch_size
    
    def is_full(self) -> bool:
        \"\"\"Check if batch is full\"\"\"
        return len(self.docs) >= self.batch_size
    
    def is_empty(self) -> bool:
        \"\"\"Check if batch is empty\"\"\"
        return len(self.docs) == 0
    
    def get_batch(self) -> List[str]:
        \"\"\"Get and clear batch\"\"\"
        docs = self.docs[:]
        self.docs.clear()
        return docs
    
    async def flush_to_lightrag(self, client: LightRAGClient) -> Dict[str, Any]:
        \"\"\"Send batch to LightRAG\"\"\"
        if self.is_empty():
            logger.warning('Attempting to flush empty batch')
            return {'processed': 0}
        
        docs = self.get_batch()
        logger.info(f'Flushing batch of {len(docs)} documents')
        
        return await client.insert_documents(documents=docs)


# ============================================================================
# 6. EXAMPLE USAGE
# ============================================================================

async def main():
    \"\"\"Example usage of LightRAG client\"\"\"
    
    # Load config from environment
    try:
        config = LightRAGConfig.from_env()
    except ConfigError as e:
        logger.error(f'Configuration error: {e}')
        logger.info('Setting LIGHTRAG_API_URL and LIGHTRAG_API_KEY environment variables')
        return
    
    # Example: Insert and query
    async with LightRAGClient(config) as client:
        # Insert example
        try:
            result = await client.insert_documents(
                documents=[
                    'Einstein developed the theory of relativity in 1905.',
                    'The theory explains the relationship between space and time.',
                ],
                doc_id='physics_basics',
            )
            logger.info(f'Insert result: {result}')
        except Exception as e:
            logger.error(f'Insert failed: {e}')
        
        # Query example
        try:
            result = await client.query(
                prompt='What is the theory of relativity?',
                mode=QueryMode.HYBRID,
                top_k=5,
            )
            logger.info(f'Query result: {result}')
        except Exception as e:
            logger.error(f'Query failed: {e}')


if __name__ == '__main__':
    # For N8N integration, export these functions:
    # - n8n_insert_document(data)
    # - n8n_query(data)
    
    # For testing locally:
    # asyncio.run(main())
    
    logger.info('LightRAG + N8N Integration Module Ready')
    logger.info('Environment variables needed:')
    logger.info('  - LIGHTRAG_API_URL')
    logger.info('  - LIGHTRAG_API_KEY')


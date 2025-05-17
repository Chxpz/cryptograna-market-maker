"""
Coletor de dados de mercado com armazenamento vetorial usando Qdrant.
"""
import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import requests
from dotenv import load_dotenv

# Configuração
load_dotenv()
logger = logging.getLogger(__name__)

class MarketDataCollector:
    def __init__(self):
        # Inicializa cliente Qdrant
        self.qdrant = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333")
        )
        
        # Configuração da coleção
        self.collection_name = "market_data"
        self.vector_size = 128  # Tamanho do vetor de features
        
        # Inicializa a coleção se não existir
        self._init_collection()
        
        # Configuração da API Helius
        self.helius_api_key = os.getenv("HELIUS_API_KEY")
        self.helius_url = f"https://api.helius.xyz/v0/token-metadata?api-key={self.helius_api_key}"
        
    def _init_collection(self):
        """Inicializa a coleção no Qdrant se não existir."""
        collections = self.qdrant.get_collections().collections
        exists = any(col.name == self.collection_name for col in collections)
        
        if not exists:
            self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Coleção {self.collection_name} criada no Qdrant")
    
    def _create_market_vector(self, data: Dict) -> np.ndarray:
        """
        Converte dados de mercado em um vetor de features.
        Em produção, isso poderia usar um modelo de embedding treinado.
        """
        # Features básicas: preço, volume, volatilidade, etc
        features = [
            data.get('price', 0),
            data.get('volume', 0),
            data.get('volatility', 0),
            data.get('bid_spread', 0),
            data.get('ask_spread', 0),
            # ... mais features
        ]
        
        # Padding para o tamanho do vetor
        features = features + [0] * (self.vector_size - len(features))
        return np.array(features, dtype=np.float32)
    
    async def collect_market_data(self) -> Dict:
        """
        Coleta dados de mercado via Helius API.
        Em produção, isso coletaria dados reais de múltiplas fontes.
        """
        try:
            # Exemplo de coleta de dados do Helius
            response = requests.get(self.helius_url)
            data = response.json()
            
            # Processa e estrutura os dados
            market_data = {
                'timestamp': datetime.now().isoformat(),
                'price': float(data.get('price', 0)),
                'volume': float(data.get('volume', 0)),
                'volatility': self._calculate_volatility(data),
                'bid_spread': float(data.get('bid_spread', 0)),
                'ask_spread': float(data.get('ask_spread', 0)),
            }
            
            # Converte para vetor e armazena
            vector = self._create_market_vector(market_data)
            self._store_data(market_data, vector)
            
            return market_data
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados: {e}")
            return {}
    
    def _calculate_volatility(self, data: Dict) -> float:
        """Calcula volatilidade baseado em dados históricos."""
        # Implementação simplificada
        return float(data.get('price_change_24h', 0)) / 100
    
    def _store_data(self, data: Dict, vector: np.ndarray):
        """Armazena dados e vetor no Qdrant."""
        try:
            self.qdrant.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=int(time.time() * 1000),  # Timestamp como ID
                        vector=vector.tolist(),
                        payload=data
                    )
                ]
            )
        except Exception as e:
            logger.error(f"Erro ao armazenar dados: {e}")
    
    async def get_similar_market_conditions(self, current_data: Dict, limit: int = 5) -> List[Dict]:
        """
        Busca condições de mercado similares no histórico.
        Útil para o modelo de IA tomar decisões baseadas em padrões históricos.
        """
        try:
            # Converte dados atuais em vetor
            vector = self._create_market_vector(current_data)
            
            # Busca pontos similares
            search_result = self.qdrant.search(
                collection_name=self.collection_name,
                query_vector=vector.tolist(),
                limit=limit
            )
            
            # Retorna os dados históricos mais similares
            return [point.payload for point in search_result]
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados similares: {e}")
            return []
    
    async def get_historical_data(self, 
                                start_time: Optional[datetime] = None,
                                end_time: Optional[datetime] = None,
                                limit: int = 100) -> List[Dict]:
        """
        Busca dados históricos em um período específico.
        """
        try:
            # Constrói filtro de tempo
            filter_condition = None
            if start_time or end_time:
                filter_condition = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="timestamp",
                            range=models.Range(
                                gt=start_time.isoformat() if start_time else None,
                                lt=end_time.isoformat() if end_time else None
                            )
                        )
                    ]
                )
            
            # Busca pontos
            search_result = self.qdrant.scroll(
                collection_name=self.collection_name,
                filter=filter_condition,
                limit=limit
            )
            
            return [point.payload for point in search_result[0]]
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados históricos: {e}")
            return [] 
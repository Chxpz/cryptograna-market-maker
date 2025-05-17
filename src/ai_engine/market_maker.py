"""
Módulo de IA para análise de mercado e geração de recomendações.
"""
import os
import logging
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Configuração
load_dotenv()
logger = logging.getLogger(__name__)

class MarketMakerAI:
    def __init__(self, collector):
        self.collector = collector
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Parâmetros de segurança
        self.min_spread = float(os.getenv("MIN_SPREAD", 0.001))
        self.max_spread = float(os.getenv("MAX_SPREAD", 0.05))
        self.max_position_size = float(os.getenv("MAX_POSITION_SIZE", 100))
        
        # Sistema de prompt para o modelo
        self.system_prompt = """Você é um especialista em market making em DEXs Solana.
        Analise os dados de mercado e recomende parâmetros para o bot de market making.
        Considere:
        1. Volatilidade do mercado
        2. Volume de trading
        3. Spread atual
        4. Condições similares no histórico
        5. Limites de segurança
        
        Retorne os parâmetros no formato JSON:
        {
            "bid_spread": float,  // Spread para ordens de compra (0.001 = 0.1%)
            "ask_spread": float,  // Spread para ordens de venda
            "order_amount": float,  // Tamanho da ordem em USD
            "inventory_target_base_pct": float  // % alvo de inventory (0-100)
        }"""
    
    async def get_recommendations(self, market_data: Dict) -> Dict:
        """
        Gera recomendações de parâmetros baseadas em dados de mercado e histórico.
        """
        try:
            # Busca condições similares no histórico
            similar_conditions = await self.collector.get_similar_market_conditions(
                market_data,
                limit=5
            )
            
            # Prepara prompt com dados atuais e históricos
            user_prompt = self._prepare_prompt(market_data, similar_conditions)
            
            # Chama OpenAI API
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Processa resposta
            recommendations = self._process_response(response.choices[0].message.content)
            
            # Valida e ajusta recomendações
            validated_recommendations = self._validate_recommendations(recommendations)
            
            logger.info(f"Recomendações geradas: {validated_recommendations}")
            return validated_recommendations
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
            return self._get_conservative_recommendations()
    
    def _prepare_prompt(self, current_data: Dict, similar_conditions: List[Dict]) -> str:
        """Prepara prompt com dados atuais e históricos."""
        prompt = f"""Dados atuais de mercado:
        - Preço: {current_data.get('price', 0)}
        - Volume: {current_data.get('volume', 0)}
        - Volatilidade: {current_data.get('volatility', 0)}
        - Spread atual: {current_data.get('bid_spread', 0)}/{current_data.get('ask_spread', 0)}
        
        Condições similares no histórico:
        {self._format_similar_conditions(similar_conditions)}
        
        Por favor, recomende parâmetros otimizados para o bot de market making."""
        
        return prompt
    
    def _format_similar_conditions(self, conditions: List[Dict]) -> str:
        """Formata condições similares para o prompt."""
        if not conditions:
            return "Nenhuma condição similar encontrada no histórico."
        
        formatted = []
        for i, condition in enumerate(conditions, 1):
            formatted.append(f"""
            Condição {i}:
            - Timestamp: {condition.get('timestamp', 'N/A')}
            - Preço: {condition.get('price', 0)}
            - Volume: {condition.get('volume', 0)}
            - Volatilidade: {condition.get('volatility', 0)}
            - Spread: {condition.get('bid_spread', 0)}/{condition.get('ask_spread', 0)}
            """)
        
        return "\n".join(formatted)
    
    def _process_response(self, response: str) -> Dict:
        """Processa resposta do modelo e extrai recomendações."""
        try:
            # Extrai JSON da resposta
            import json
            recommendations = json.loads(response)
            return recommendations
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return self._get_conservative_recommendations()
    
    def _validate_recommendations(self, recommendations: Dict) -> Dict:
        """Valida e ajusta recomendações para garantir segurança."""
        validated = recommendations.copy()
        
        # Valida spreads
        validated['bid_spread'] = max(
            min(float(validated.get('bid_spread', self.min_spread)), self.max_spread),
            self.min_spread
        )
        validated['ask_spread'] = max(
            min(float(validated.get('ask_spread', self.min_spread)), self.max_spread),
            self.min_spread
        )
        
        # Valida tamanho da ordem
        validated['order_amount'] = min(
            float(validated.get('order_amount', self.max_position_size/2)),
            self.max_position_size
        )
        
        # Valida target de inventory
        validated['inventory_target_base_pct'] = max(
            min(float(validated.get('inventory_target_base_pct', 50)), 100),
            0
        )
        
        return validated
    
    def _get_conservative_recommendations(self) -> Dict:
        """Retorna recomendações conservadoras em caso de erro."""
        return {
            "bid_spread": self.min_spread * 2,
            "ask_spread": self.min_spread * 2,
            "order_amount": self.max_position_size * 0.1,
            "inventory_target_base_pct": 50.0
        } 
"""
Market Structure Analysis Module
Implements various market structures: perfect competition, monopoly, oligopoly, monopolistic competition
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class MarketStructures:
    def __init__(self):
        pass
    
    def perfect_competition(self, a, b, mc):
        """
        Perfect competition equilibrium
        Demand: P = a - bQ
        Supply: P = MC
        """
        # Equilibrium: a - bQ = mc
        q_eq = (a - mc) / b
        p_eq = mc
        
        # Consumer surplus = 0.5 * base * height = 0.5 * Q * (a - P)
        consumer_surplus = 0.5 * q_eq * (a - p_eq)
        
        # Producer surplus = 0 (P = MC)
        producer_surplus = 0
        
        return {
            'price': p_eq,
            'quantity': q_eq,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': producer_surplus,
            'total_surplus': consumer_surplus + producer_surplus,
            'market_type': 'Perfect Competition'
        }
    
    def monopoly(self, a, b, mc):
        """
        Monopoly equilibrium
        Demand: P = a - bQ
        MR = a - 2bQ
        MC = mc
        """
        # Equilibrium: MR = MC -> a - 2bQ = mc
        q_eq = (a - mc) / (2 * b)
        p_eq = a - b * q_eq
        
        # Consumer surplus
        consumer_surplus = 0.5 * q_eq * (a - p_eq)
        
        # Producer surplus = (P - MC) * Q
        producer_surplus = (p_eq - mc) * q_eq
        
        # Deadweight loss compared to perfect competition
        q_competitive = (a - mc) / b
        deadweight_loss = 0.5 * b * (q_competitive - q_eq)**2
        
        return {
            'price': p_eq,
            'quantity': q_eq,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': producer_surplus,
            'total_surplus': consumer_surplus + producer_surplus,
            'deadweight_loss': deadweight_loss,
            'market_type': 'Monopoly'
        }
    
    def cournot_oligopoly(self, a, b, mc, n_firms):
        """
        Cournot oligopoly with n symmetric firms
        Each firm chooses quantity simultaneously
        """
        # Equilibrium quantity per firm: qi = (a - mc) / (b(n+1))
        q_per_firm = (a - mc) / (b * (n_firms + 1))
        q_total = n_firms * q_per_firm
        p_eq = a - b * q_total
        
        # Profits per firm
        profit_per_firm = (p_eq - mc) * q_per_firm
        total_producer_surplus = n_firms * profit_per_firm
        
        # Consumer surplus
        consumer_surplus = 0.5 * q_total * (a - p_eq)
        
        return {
            'price': p_eq,
            'quantity': q_total,
            'quantity_per_firm': q_per_firm,
            'profit_per_firm': profit_per_firm,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': total_producer_surplus,
            'total_surplus': consumer_surplus + total_producer_surplus,
            'n_firms': n_firms,
            'market_type': f'Cournot Oligopoly ({n_firms} firms)'
        }
    
    def monopolistic_competition(self, a, b, mc):
        """
        Monopolistic competition (simplified)
        Each firm has some market power but free entry drives profits to zero
        """
        # In long-run equilibrium, P = AC (zero economic profit)
        # Assuming AC = MC (constant returns)
        # But firms still have downward-sloping demand curves
        
        # Simplified: firms price above MC but competition limits markup
        markup = 0.2  # 20% markup over MC
        p_eq = mc * (1 + markup)
        q_eq = (a - p_eq) / b
        
        # Consumer surplus
        consumer_surplus = 0.5 * q_eq * (a - p_eq)
        
        # Producer surplus approaches zero in long run
        producer_surplus = 0.1 * q_eq  # Small positive profit
        
        return {
            'price': p_eq,
            'quantity': q_eq,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': producer_surplus,
            'total_surplus': consumer_surplus + producer_surplus,
            'markup': markup,
            'market_type': 'Monopolistic Competition'
        }
    
    def plot_market_equilibrium(self, result, a, b, mc):
        """
        Plot supply and demand curves with equilibrium point
        """
        # Create quantity range
        q_max = a / b
        q_range = np.linspace(0, q_max, 100)
        
        # Demand curve: P = a - bQ
        demand_curve = a - b * q_range
        
        # Supply curve (varies by market type)
        if result['market_type'] == 'Perfect Competition':
            supply_curve = np.full_like(q_range, mc)
        else:
            # For other market types, show MC curve
            supply_curve = np.full_like(q_range, mc)
        
        # Create plot
        fig = go.Figure()
        
        # Add demand curve
        fig.add_trace(go.Scatter(
            x=q_range, y=demand_curve,
            mode='lines',
            name='Demand',
            line=dict(color='blue', width=2)
        ))
        
        # Add supply/MC curve
        fig.add_trace(go.Scatter(
            x=q_range, y=supply_curve,
            mode='lines',
            name='Supply/MC',
            line=dict(color='red', width=2)
        ))
        
        # Add equilibrium point
        fig.add_trace(go.Scatter(
            x=[result['quantity']], y=[result['price']],
            mode='markers',
            name='Equilibrium',
            marker=dict(color='green', size=10, symbol='circle')
        ))
        
        # Add MR curve for monopoly
        if result['market_type'] == 'Monopoly':
            mr_curve = a - 2 * b * q_range
            fig.add_trace(go.Scatter(
                x=q_range, y=mr_curve,
                mode='lines',
                name='Marginal Revenue',
                line=dict(color='orange', width=2, dash='dash')
            ))
        
        # Highlight consumer surplus
        cs_q = np.linspace(0, result['quantity'], 50)
        cs_upper = a - b * cs_q
        cs_lower = np.full_like(cs_q, result['price'])
        
        fig.add_trace(go.Scatter(
            x=np.concatenate([cs_q, cs_q[::-1]]),
            y=np.concatenate([cs_upper, cs_lower[::-1]]),
            fill='toself',
            fillcolor='rgba(0, 100, 255, 0.3)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Consumer Surplus',
            showlegend=True
        ))
        
        # Highlight producer surplus (if any)
        if result['producer_surplus'] > 0:
            ps_q = np.linspace(0, result['quantity'], 50)
            ps_upper = np.full_like(ps_q, result['price'])
            ps_lower = np.full_like(ps_q, mc)
            
            fig.add_trace(go.Scatter(
                x=np.concatenate([ps_q, ps_q[::-1]]),
                y=np.concatenate([ps_upper, ps_lower[::-1]]),
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.3)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Producer Surplus',
                showlegend=True
            ))
        
        # Update layout
        fig.update_layout(
            title=f'{result["market_type"]} - Market Equilibrium',
            xaxis_title='Quantity',
            yaxis_title='Price',
            hovermode='x',
            showlegend=True,
            height=500
        )
        
        return fig
    
    def compare_market_structures(self, a, b, mc, n_firms=3):
        """
        Compare outcomes across different market structures
        """
        pc = self.perfect_competition(a, b, mc)
        monopoly = self.monopoly(a, b, mc)
        oligopoly = self.cournot_oligopoly(a, b, mc, n_firms)
        mono_comp = self.monopolistic_competition(a, b, mc)
        
        comparison = {
            'Perfect Competition': pc,
            'Monopoly': monopoly,
            f'Oligopoly ({n_firms} firms)': oligopoly,
            'Monopolistic Competition': mono_comp
        }
        
        return comparison 
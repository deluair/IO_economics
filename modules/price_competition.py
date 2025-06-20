"""
Price Competition Models Module
Implements Bertrand, Cournot, and Stackelberg competition
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class PriceCompetition:
    def __init__(self):
        pass
    
    def bertrand_competition(self, mc1, mc2, a, b, gamma=0.5):
        """
        Bertrand price competition with differentiated products
        Demand functions:
        q1 = a - b*p1 + gamma*b*p2
        q2 = a - b*p2 + gamma*b*p1
        
        gamma: degree of substitutability (0 = independent, 1 = perfect substitutes)
        """
        # Solve for Nash equilibrium prices
        # FOC: dπ1/dp1 = q1 + p1*dq1/dp1 - mc1*dq1/dp1 = 0
        # This gives: a - b*p1 + gamma*b*p2 + (p1 - mc1)*(-b) = 0
        # Simplifying: a - 2*b*p1 + gamma*b*p2 + b*mc1 = 0
        # p1 = (a + gamma*b*p2 + b*mc1) / (2*b)
        
        # Solving the system of equations:
        denominator = 4 - gamma**2
        p1 = (2*a + 2*b*mc1 + gamma*b*mc2) / (b * denominator)
        p2 = (2*a + 2*b*mc2 + gamma*b*mc1) / (b * denominator)
        
        # Calculate quantities
        q1 = a - b*p1 + gamma*b*p2
        q2 = a - b*p2 + gamma*b*p1
        
        # Calculate profits
        profit1 = (p1 - mc1) * q1
        profit2 = (p2 - mc2) * q2
        
        # Consumer surplus (approximate)
        consumer_surplus = 0.5 * b * (q1**2 + q2**2) + gamma * b * q1 * q2
        
        return {
            'price1': p1,
            'price2': p2,
            'quantity1': q1,
            'quantity2': q2,
            'profit1': profit1,
            'profit2': profit2,
            'total_quantity': q1 + q2,
            'consumer_surplus': consumer_surplus,
            'differentiation': gamma,
            'competition_type': 'Bertrand'
        }
    
    def cournot_competition(self, mc1, mc2, a, b):
        """
        Cournot quantity competition
        Inverse demand: P = a - b*(q1 + q2)
        """
        # Reaction functions:
        # π1 = (a - b*(q1 + q2) - mc1) * q1
        # FOC: a - b*q2 - 2*b*q1 - mc1 = 0
        # q1 = (a - mc1 - b*q2) / (2*b)
        
        # Solving simultaneously:
        q1 = (a - 2*mc1 + mc2) / (3*b)
        q2 = (a - 2*mc2 + mc1) / (3*b)
        
        # Market price
        price = a - b*(q1 + q2)
        
        # Profits
        profit1 = (price - mc1) * q1
        profit2 = (price - mc2) * q2
        
        # Consumer surplus
        total_quantity = q1 + q2
        consumer_surplus = 0.5 * total_quantity * (a - price)
        
        return {
            'price1': price,
            'price2': price,
            'quantity1': q1,
            'quantity2': q2,
            'profit1': profit1,
            'profit2': profit2,
            'market_price': price,
            'total_quantity': total_quantity,
            'consumer_surplus': consumer_surplus,
            'competition_type': 'Cournot'
        }
    
    def stackelberg_competition(self, mc1, mc2, a, b, leader='Firm 1'):
        """
        Stackelberg sequential quantity competition
        """
        if leader == 'Firm 1':
            # Firm 1 is leader, Firm 2 is follower
            # Firm 2's reaction function: q2 = (a - mc2 - b*q1) / (2*b)
            # Firm 1 maximizes knowing this reaction function
            # π1 = (a - b*q1 - b*q2 - mc1)*q1
            # Substitute q2: π1 = (a - b*q1 - b*(a - mc2 - b*q1)/(2*b) - mc1)*q1
            # Simplifying: q1 = (a - 2*mc1 + mc2) / (2*b)
            
            q1 = (a - 2*mc1 + mc2) / (2*b)
            q2 = (a - mc2 - b*q1) / (2*b)
        else:
            # Firm 2 is leader, Firm 1 is follower
            q2 = (a - 2*mc2 + mc1) / (2*b)
            q1 = (a - mc1 - b*q2) / (2*b)
        
        # Market price
        price = a - b*(q1 + q2)
        
        # Profits
        profit1 = (price - mc1) * q1
        profit2 = (price - mc2) * q2
        
        # Consumer surplus
        total_quantity = q1 + q2
        consumer_surplus = 0.5 * total_quantity * (a - price)
        
        return {
            'price1': price,
            'price2': price,
            'quantity1': q1,
            'quantity2': q2,
            'profit1': profit1,
            'profit2': profit2,
            'market_price': price,
            'total_quantity': total_quantity,
            'consumer_surplus': consumer_surplus,
            'leader': leader,
            'competition_type': 'Stackelberg'
        }
    
    def plot_competition_outcomes(self, result, competition_type):
        """
        Visualize competition outcomes
        """
        if competition_type == 'Bertrand Competition':
            return self._plot_bertrand_outcomes(result)
        elif competition_type == 'Cournot Competition':
            return self._plot_cournot_outcomes(result)
        else:  # Stackelberg
            return self._plot_stackelberg_outcomes(result)
    
    def _plot_bertrand_outcomes(self, result):
        """Plot Bertrand competition results"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Prices', 'Quantities', 'Profits', 'Market Shares'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        firms = ['Firm 1', 'Firm 2']
        
        # Prices
        fig.add_trace(
            go.Bar(x=firms, y=[result['price1'], result['price2']], name='Price'),
            row=1, col=1
        )
        
        # Quantities
        fig.add_trace(
            go.Bar(x=firms, y=[result['quantity1'], result['quantity2']], name='Quantity'),
            row=1, col=2
        )
        
        # Profits
        fig.add_trace(
            go.Bar(x=firms, y=[result['profit1'], result['profit2']], name='Profit'),
            row=2, col=1
        )
        
        # Market shares
        total_q = result['quantity1'] + result['quantity2']
        shares = [result['quantity1']/total_q, result['quantity2']/total_q]
        fig.add_trace(
            go.Pie(labels=firms, values=shares, name='Market Share'),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f"Bertrand Competition Results (γ={result['differentiation']:.2f})",
            showlegend=False,
            height=600
        )
        
        return fig
    
    def _plot_cournot_outcomes(self, result):
        """Plot Cournot competition results"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quantities', 'Profits', 'Market Share', 'Price Comparison'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        firms = ['Firm 1', 'Firm 2']
        
        # Quantities
        fig.add_trace(
            go.Bar(x=firms, y=[result['quantity1'], result['quantity2']], name='Quantity'),
            row=1, col=1
        )
        
        # Profits
        fig.add_trace(
            go.Bar(x=firms, y=[result['profit1'], result['profit2']], name='Profit'),
            row=1, col=2
        )
        
        # Market shares
        total_q = result['quantity1'] + result['quantity2']
        shares = [result['quantity1']/total_q, result['quantity2']/total_q]
        fig.add_trace(
            go.Pie(labels=firms, values=shares, name='Market Share'),
            row=2, col=1
        )
        
        # Price (same for both firms in Cournot)
        fig.add_trace(
            go.Bar(x=['Market Price'], y=[result['market_price']], name='Price'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Cournot Competition Results",
            showlegend=False,
            height=600
        )
        
        return fig
    
    def _plot_stackelberg_outcomes(self, result):
        """Plot Stackelberg competition results"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quantities', 'Profits', 'Market Share', 'Leader Advantage'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        firms = ['Firm 1', 'Firm 2']
        colors = ['gold' if result['leader'] == 'Firm 1' else 'lightblue',
                 'gold' if result['leader'] == 'Firm 2' else 'lightblue']
        
        # Quantities
        fig.add_trace(
            go.Bar(x=firms, y=[result['quantity1'], result['quantity2']], 
                  marker_color=colors, name='Quantity'),
            row=1, col=1
        )
        
        # Profits
        fig.add_trace(
            go.Bar(x=firms, y=[result['profit1'], result['profit2']], 
                  marker_color=colors, name='Profit'),
            row=1, col=2
        )
        
        # Market shares
        total_q = result['quantity1'] + result['quantity2']
        shares = [result['quantity1']/total_q, result['quantity2']/total_q]
        fig.add_trace(
            go.Pie(labels=firms, values=shares, name='Market Share'),
            row=2, col=1
        )
        
        # Leader vs Follower comparison
        leader_profit = result['profit1'] if result['leader'] == 'Firm 1' else result['profit2']
        follower_profit = result['profit2'] if result['leader'] == 'Firm 1' else result['profit1']
        
        fig.add_trace(
            go.Bar(x=['Leader', 'Follower'], y=[leader_profit, follower_profit], 
                  marker_color=['gold', 'lightblue'], name='Profit by Role'),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f"Stackelberg Competition Results (Leader: {result['leader']})",
            showlegend=False,
            height=600
        )
        
        return fig
    
    def compare_competition_types(self, mc1, mc2, a, b):
        """
        Compare outcomes across different competition types
        """
        bertrand = self.bertrand_competition(mc1, mc2, a, b, gamma=0.5)
        cournot = self.cournot_competition(mc1, mc2, a, b)
        stackelberg1 = self.stackelberg_competition(mc1, mc2, a, b, 'Firm 1')
        stackelberg2 = self.stackelberg_competition(mc1, mc2, a, b, 'Firm 2')
        
        comparison = {
            'Bertrand': bertrand,
            'Cournot': cournot,
            'Stackelberg (Firm 1 Leader)': stackelberg1,
            'Stackelberg (Firm 2 Leader)': stackelberg2
        }
        
        return comparison 
"""
Product Differentiation Module
Implements spatial competition models (Hotelling) and vertical differentiation
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class ProductDifferentiation:
    def __init__(self):
        pass
    
    def hotelling_linear_city(self, transport_cost, marginal_cost, city_length=1):
        """
        Hotelling's linear city model
        Firms choose locations and prices on a line of length city_length
        """
        # In equilibrium with endogenous locations:
        # Firms locate at 1/4 and 3/4 of the city length
        # This is the solution to the two-stage game (location then price)
        
        location1 = city_length / 4
        location2 = 3 * city_length / 4
        
        # Equilibrium prices (with symmetric firms)
        # p* = mc + t * city_length
        price1 = marginal_cost + transport_cost * city_length
        price2 = marginal_cost + transport_cost * city_length
        
        # Market shares (equal in symmetric equilibrium)
        market_share1 = 0.5
        market_share2 = 0.5
        
        # Consumer at location x is indifferent between firms when:
        # p1 + t*|x - x1| = p2 + t*|x - x2|
        indifferent_consumer = city_length / 2
        
        # Profits
        demand1 = market_share1 * city_length  # Assuming unit density
        demand2 = market_share2 * city_length
        
        profit1 = (price1 - marginal_cost) * demand1
        profit2 = (price2 - marginal_cost) * demand2
        
        # Total transport costs (welfare loss)
        # Integral of transport costs paid by all consumers
        transport_costs = transport_cost * city_length**2 / 12  # Analytical result
        
        return {
            'location1': location1,
            'location2': location2,
            'price1': price1,
            'price2': price2,
            'market_share1': market_share1,
            'market_share2': market_share2,
            'profit1': profit1,
            'profit2': profit2,
            'indifferent_consumer': indifferent_consumer,
            'total_transport_costs': transport_costs,
            'city_length': city_length,
            'model_type': 'Hotelling Linear City'
        }
    
    def circular_city_model(self, transport_cost, marginal_cost, n_firms=3):
        """
        Circular city model (Salop model)
        Firms are equally spaced around a circle
        """
        # In symmetric equilibrium with n firms
        # Distance between adjacent firms = 1/n
        firm_spacing = 1.0 / n_firms
        
        # Equilibrium price
        # p* = mc + t/(2n) (for large n, approaches mc)
        price = marginal_cost + transport_cost / (2 * n_firms)
        
        # Market share per firm
        market_share = 1.0 / n_firms
        
        # Profit per firm
        profit_per_firm = (price - marginal_cost) * market_share
        
        # Consumer surplus (approximate)
        # Lower when more firms due to variety, but higher due to competition
        consumer_surplus = 0.5 * market_share * (transport_cost / (2 * n_firms))
        
        return {
            'n_firms': n_firms,
            'firm_spacing': firm_spacing,
            'price': price,
            'market_share_per_firm': market_share,
            'profit_per_firm': profit_per_firm,
            'total_profit': n_firms * profit_per_firm,
            'consumer_surplus_per_firm': consumer_surplus,
            'model_type': 'Circular City'
        }
    
    def vertical_differentiation(self, quality_high, quality_low, cost_high, cost_low):
        """
        Vertical differentiation model
        Two products with different qualities and costs
        """
        # Assume consumer preferences: U = θ*q - p
        # where θ is consumer type (willingness to pay for quality)
        # θ is uniformly distributed on [0, 1]
        
        # In equilibrium, firms set prices:
        # Marginal consumer θ* is indifferent between products
        # High-quality firm serves [θ*, 1], low-quality serves [0, θ*]
        
        # Equilibrium prices (derived from profit maximization)
        quality_diff = quality_high - quality_low
        
        # If both firms serve the market:
        if quality_diff > 0:
            # Price for high quality product
            price_high = cost_high + (2 * quality_high - quality_low) / 3
            
            # Price for low quality product  
            price_low = cost_low + (2 * quality_low - quality_high) / 3
            
            # Marginal consumer (indifferent between products)
            theta_star = (price_high - price_low) / quality_diff
            
            # Demands
            demand_high = max(0, 1 - theta_star)
            demand_low = max(0, theta_star)
            
            # Ensure non-negative demands
            if demand_high < 0:
                demand_high = 0
                price_high = cost_high
            if demand_low < 0:
                demand_low = 0  
                price_low = cost_low
                
        else:
            # If qualities are the same, standard Bertrand competition
            price_high = max(cost_high, cost_low)
            price_low = max(cost_high, cost_low)
            demand_high = 0.5
            demand_low = 0.5
            theta_star = 0.5
        
        # Profits
        profit_high = max(0, (price_high - cost_high) * demand_high)
        profit_low = max(0, (price_low - cost_low) * demand_low)
        
        return {
            'quality_high': quality_high,
            'quality_low': quality_low,
            'price_high': price_high,
            'price_low': price_low,
            'demand_high': demand_high,
            'demand_low': demand_low,
            'profit_high': profit_high,
            'profit_low': profit_low,
            'marginal_consumer': theta_star,
            'quality_premium': price_high - price_low,
            'model_type': 'Vertical Differentiation'
        }
    
    def plot_hotelling_model(self, result, city_length):
        """
        Visualize Hotelling linear city model
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Firm Locations', 'Price Competition', 
                           'Market Shares', 'Consumer Utility'),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "scatter"}]]
        )
        
        # Firm locations on the line
        fig.add_trace(
            go.Scatter(
                x=[result['location1'], result['location2']], 
                y=[0, 0],
                mode='markers+text',
                marker=dict(size=15, color=['red', 'blue']),
                text=['Firm 1', 'Firm 2'],
                textposition='top center',
                name='Firm Locations'
            ),
            row=1, col=1
        )
        
        # Add city line
        fig.add_trace(
            go.Scatter(
                x=[0, city_length], y=[0, 0],
                mode='lines',
                line=dict(color='black', width=2),
                name='City'
            ),
            row=1, col=1
        )
        
        # Prices
        fig.add_trace(
            go.Bar(x=['Firm 1', 'Firm 2'], 
                  y=[result['price1'], result['price2']], 
                  name='Prices'),
            row=1, col=2
        )
        
        # Market shares
        fig.add_trace(
            go.Pie(labels=['Firm 1', 'Firm 2'], 
                  values=[result['market_share1'], result['market_share2']], 
                  name='Market Share'),
            row=2, col=1
        )
        
        # Consumer utility across locations (need to get transport_cost from result context)
        x_locations = np.linspace(0, city_length, 100)
        # Approximate transport cost for visualization
        transport_cost_approx = (result['price1'] - city_length/4) / city_length if city_length > 0 else 1
        utility1 = -(result['price1'] + transport_cost_approx * np.abs(x_locations - result['location1']))
        utility2 = -(result['price2'] + transport_cost_approx * np.abs(x_locations - result['location2']))
        
        fig.add_trace(
            go.Scatter(x=x_locations, y=utility1, name='Utility from Firm 1', 
                      line=dict(color='red')),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=x_locations, y=utility2, name='Utility from Firm 2', 
                      line=dict(color='blue')),
            row=2, col=2
        )
        
        # Mark indifferent consumer
        fig.add_trace(
            go.Scatter(x=[result['indifferent_consumer']], y=[0], 
                      mode='markers',
                      marker=dict(size=10, color='green'),
                      name='Indifferent Consumer'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Hotelling Linear City Model",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def plot_vertical_differentiation(self, result):
        """
        Visualize vertical differentiation model
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Quality vs Price', 'Market Demands', 
                           'Profits', 'Consumer Segmentation'),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Quality vs Price scatter
        fig.add_trace(
            go.Scatter(
                x=[result['quality_low'], result['quality_high']], 
                y=[result['price_low'], result['price_high']],
                mode='markers+text',
                marker=dict(size=[30, 40], color=['orange', 'red']),
                text=['Low Quality', 'High Quality'],
                textposition='top center',
                name='Products'
            ),
            row=1, col=1
        )
        
        # Market demands
        fig.add_trace(
            go.Bar(x=['Low Quality', 'High Quality'], 
                  y=[result['demand_low'], result['demand_high']], 
                  name='Demand'),
            row=1, col=2
        )
        
        # Profits
        fig.add_trace(
            go.Bar(x=['Low Quality', 'High Quality'], 
                  y=[result['profit_low'], result['profit_high']], 
                  name='Profit'),
            row=2, col=1
        )
        
        # Consumer segmentation
        theta_range = np.linspace(0, 1, 100)
        utility_high = theta_range * result['quality_high'] - result['price_high']
        utility_low = theta_range * result['quality_low'] - result['price_low']
        
        fig.add_trace(
            go.Scatter(x=theta_range, y=utility_high, name='Utility from High Quality', 
                      line=dict(color='red')),
            row=2, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=theta_range, y=utility_low, name='Utility from Low Quality', 
                      line=dict(color='orange')),
            row=2, col=2
        )
        
        # Mark marginal consumer
        if 0 <= result['marginal_consumer'] <= 1:
            fig.add_trace(
                go.Scatter(x=[result['marginal_consumer']], y=[0], 
                          mode='markers',
                          marker=dict(size=10, color='green'),
                          name='Marginal Consumer'),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Vertical Differentiation Model",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def welfare_analysis(self, result):
        """
        Analyze welfare implications of product differentiation
        """
        if result['model_type'] == 'Hotelling Linear City':
            # Consumer surplus = Total utility - Total payments - Transport costs
            total_revenue = (result['price1'] * result['market_share1'] * result['city_length'] +
                           result['price2'] * result['market_share2'] * result['city_length'])
            
            producer_surplus = result['profit1'] + result['profit2']
            
            # Consumer surplus (approximate)
            consumer_surplus = -result['total_transport_costs']  # Negative of transport costs
            
            total_welfare = producer_surplus + consumer_surplus
            
        elif result['model_type'] == 'Vertical Differentiation':
            producer_surplus = result['profit_high'] + result['profit_low']
            
            # Consumer surplus calculation for vertical differentiation
            # Integral of consumer utilities
            theta_star = result['marginal_consumer']
            
            # High-quality consumers: integral from theta_star to 1
            cs_high = (theta_star * result['quality_high'] - result['price_high']) * (1 - theta_star) / 2
            
            # Low-quality consumers: integral from 0 to theta_star  
            cs_low = (theta_star * result['quality_low'] - result['price_low']) * theta_star / 2
            
            consumer_surplus = max(0, cs_high + cs_low)
            total_welfare = producer_surplus + consumer_surplus
        
        else:
            producer_surplus = 0
            consumer_surplus = 0
            total_welfare = 0
        
        return {
            'producer_surplus': producer_surplus,
            'consumer_surplus': consumer_surplus,
            'total_welfare': total_welfare,
            'welfare_components': {
                'producer': producer_surplus,
                'consumer': consumer_surplus
            }
        } 
"""
Network Effects Module
Implements platform competition, network adoption dynamics, and two-sided markets
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class NetworkEffects:
    def __init__(self):
        pass
    
    def platform_competition(self, network_strength, platform1_quality, platform2_quality, total_users=1000):
        """
        Competition between two platforms with network effects
        """
        # Users choose platform based on: utility = platform_quality + network_strength * network_size
        # In equilibrium, marginal user is indifferent between platforms
        
        # Let x be the share of users on platform 1
        # Utility from platform 1: q1 + β * x * N
        # Utility from platform 2: q2 + β * (1-x) * N
        # Indifferent user: q1 + β * x * N = q2 + β * (1-x) * N
        
        # Solving for equilibrium market share:
        # q1 + β * x * N = q2 + β * N - β * x * N
        # q1 - q2 = β * N - 2 * β * x * N
        # x = (β * N + q2 - q1) / (2 * β * N)
        
        if network_strength > 0:
            market_share1 = (network_strength * total_users + platform2_quality - platform1_quality) / (2 * network_strength * total_users)
        else:
            # No network effects - pure quality competition
            if platform1_quality > platform2_quality:
                market_share1 = 1.0
            elif platform2_quality > platform1_quality:
                market_share1 = 0.0
            else:
                market_share1 = 0.5
        
        # Ensure market shares are between 0 and 1
        market_share1 = max(0, min(1, market_share1))
        market_share2 = 1 - market_share1
        
        users1 = market_share1 * total_users
        users2 = market_share2 * total_users
        
        # Network values
        network_value1 = network_strength * users1
        network_value2 = network_strength * users2
        
        # Total utility per user
        utility1 = platform1_quality + network_value1
        utility2 = platform2_quality + network_value2
        
        return {
            'market_share1': market_share1,
            'market_share2': market_share2,
            'users1': users1,
            'users2': users2,
            'network_value1': network_value1,
            'network_value2': network_value2,
            'utility1': utility1,
            'utility2': utility2,
            'total_users': total_users,
            'model_type': 'Platform Competition'
        }
    
    def network_adoption_dynamics(self, adoption_threshold, network_value, population_size, time_periods=50):
        """
        Simulate network adoption over time with critical mass dynamics
        """
        adoption_history = []
        current_adopters = population_size * 0.01  # Start with 1% early adopters
        
        for t in range(time_periods):
            adoption_rate = current_adopters / population_size
            adoption_history.append(adoption_rate)
            
            # Network utility increases with adoption
            network_utility = network_value * adoption_rate
            
            # Probability of new adoption depends on network utility and threshold
            if network_utility > adoption_threshold:
                # Above threshold - adoption accelerates
                growth_rate = 0.1 * (network_utility - adoption_threshold)
                new_adopters = min(population_size - current_adopters, 
                                 growth_rate * (population_size - current_adopters))
            else:
                # Below threshold - slow adoption
                growth_rate = 0.02
                new_adopters = growth_rate * (population_size - current_adopters)
            
            current_adopters += new_adopters
            
            # Stop if full adoption reached
            if current_adopters >= population_size * 0.99:
                break
        
        final_adoption = current_adopters / population_size
        
        # Find time to critical mass (50% adoption)
        critical_mass_time = time_periods
        for i, rate in enumerate(adoption_history):
            if rate >= 0.5:
                critical_mass_time = i
                break
        
        return {
            'adoption_history': adoption_history,
            'time_periods': list(range(len(adoption_history))),
            'final_adoption': final_adoption,
            'critical_mass_time': critical_mass_time,
            'population_size': population_size,
            'model_type': 'Network Adoption'
        }
    
    def two_sided_market(self, cross_network_effect, platform_cost, max_users_per_side=1000):
        """
        Two-sided market with cross-network effects
        """
        # Platform sets prices for both sides to maximize profit
        # User utility: u_a = v_a - p_a + β * n_b (for side A users)
        # User utility: u_b = v_b - p_b + β * n_a (for side B users)
        
        # Assume symmetric sides with v_a = v_b = 1
        base_value = 1.0
        
        # Optimal pricing with cross-network effects
        # Platform internalizes network externalities
        
        # Simplified equilibrium: platform may subsidize one side
        if cross_network_effect > 0.5:
            # Strong network effects - subsidize one side
            price_a = 0.1  # Low price for side A
            price_b = 0.8  # Higher price for side B
        else:
            # Weak network effects - symmetric pricing
            price_a = 0.4
            price_b = 0.4
        
        # Demand functions (simplified)
        # n_a = α * (v_a - p_a + β * n_b)
        # n_b = α * (v_b - p_b + β * n_a)
        
        # Solving system of equations
        denominator = 1 - cross_network_effect**2
        if denominator > 0:
            users_a = max_users_per_side * (base_value - price_a + cross_network_effect * (base_value - price_b)) / denominator
            users_b = max_users_per_side * (base_value - price_b + cross_network_effect * (base_value - price_a)) / denominator
        else:
            users_a = max_users_per_side / 2
            users_b = max_users_per_side / 2
        
        # Ensure non-negative users
        users_a = max(0, min(max_users_per_side, users_a))
        users_b = max(0, min(max_users_per_side, users_b))
        
        # Platform revenue and profit
        revenue = price_a * users_a + price_b * users_b
        profit = revenue - platform_cost
        
        # Network values
        network_value_a = cross_network_effect * users_b
        network_value_b = cross_network_effect * users_a
        
        return {
            'users_a': users_a,
            'users_b': users_b,
            'price_a': price_a,
            'price_b': price_b,
            'revenue': revenue,
            'profit': profit,
            'network_value_a': network_value_a,
            'network_value_b': network_value_b,
            'cross_network_effect': cross_network_effect,
            'model_type': 'Two-Sided Market'
        }
    
    def network_externality_welfare(self, network_strength, adoption_rate, population_size):
        """
        Calculate welfare effects of network externalities
        """
        active_users = adoption_rate * population_size
        
        # Each user's utility includes network benefit
        individual_network_benefit = network_strength * active_users
        
        # Total network value (with and without externality internalization)
        total_network_value = active_users * individual_network_benefit
        
        # Deadweight loss from network externalities not being internalized
        # Users don't consider their effect on others when joining
        optimal_adoption = min(1.0, adoption_rate * (1 + network_strength))
        optimal_users = optimal_adoption * population_size
        
        deadweight_loss = 0.5 * network_strength * (optimal_users - active_users)**2
        
        return {
            'current_adoption': adoption_rate,
            'optimal_adoption': optimal_adoption,
            'network_value_per_user': individual_network_benefit,
            'total_network_value': total_network_value,
            'deadweight_loss': deadweight_loss,
            'welfare_gain_from_coordination': deadweight_loss
        }
    
    def platform_pricing_strategy(self, network_strength, marginal_cost, competition_intensity=0.5):
        """
        Analyze optimal pricing strategy for platforms with network effects
        """
        # Platform faces trade-off: lower prices increase adoption and network value
        # but reduce per-user profit
        
        # Optimal price depends on network strength
        if network_strength > 1:
            # Strong network effects - penetration pricing
            optimal_price = marginal_cost * 0.8  # Price below cost initially
            strategy = "Penetration Pricing"
        elif network_strength > 0.5:
            # Medium network effects - competitive pricing  
            optimal_price = marginal_cost * (1 + 0.2 / competition_intensity)
            strategy = "Competitive Pricing"
        else:
            # Weak network effects - profit maximization
            optimal_price = marginal_cost * 2
            strategy = "Profit Maximization"
        
        # Expected market share based on pricing strategy
        if strategy == "Penetration Pricing":
            expected_market_share = 0.7
        elif strategy == "Competitive Pricing":
            expected_market_share = 0.5
        else:
            expected_market_share = 0.3
        
        # Long-term profit calculation
        users = expected_market_share * 1000  # Assume 1000 total users
        revenue = optimal_price * users
        costs = marginal_cost * users
        profit = revenue - costs
        
        return {
            'optimal_price': optimal_price,
            'strategy': strategy,
            'expected_market_share': expected_market_share,
            'expected_users': users,
            'expected_profit': profit,
            'network_strength': network_strength
        }
    
    def plot_adoption_dynamics(self, result):
        """
        Plot network adoption over time
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=result['time_periods'],
            y=result['adoption_history'],
            mode='lines+markers',
            name='Adoption Rate',
            line=dict(color='blue', width=3)
        ))
        
        # Add critical mass line
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", 
                     annotation_text="Critical Mass (50%)")
        
        # Mark critical mass time
        if result['critical_mass_time'] < len(result['time_periods']):
            fig.add_vline(x=result['critical_mass_time'], line_dash="dash", 
                         line_color="orange", 
                         annotation_text=f"Critical Mass at t={result['critical_mass_time']}")
        
        fig.update_layout(
            title="Network Adoption Dynamics",
            xaxis_title="Time Period",
            yaxis_title="Adoption Rate",
            height=400,
            showlegend=True
        )
        
        return fig
    
    def plot_platform_competition(self, result):
        """
        Visualize platform competition results
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Market Shares', 'User Counts', 'Network Values', 'Total Utilities'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        platforms = ['Platform 1', 'Platform 2']
        
        # Market shares
        fig.add_trace(
            go.Pie(labels=platforms, 
                  values=[result['market_share1'], result['market_share2']], 
                  name='Market Share'),
            row=1, col=1
        )
        
        # User counts
        fig.add_trace(
            go.Bar(x=platforms, y=[result['users1'], result['users2']], 
                  name='Users'),
            row=1, col=2
        )
        
        # Network values
        fig.add_trace(
            go.Bar(x=platforms, y=[result['network_value1'], result['network_value2']], 
                  name='Network Value'),
            row=2, col=1
        )
        
        # Total utilities
        fig.add_trace(
            go.Bar(x=platforms, y=[result['utility1'], result['utility2']], 
                  name='Total Utility'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Platform Competition Analysis",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def plot_two_sided_market(self, result):
        """
        Visualize two-sided market results
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('User Counts', 'Prices', 'Network Values', 'Revenue Breakdown'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        sides = ['Side A', 'Side B']
        
        # User counts
        fig.add_trace(
            go.Bar(x=sides, y=[result['users_a'], result['users_b']], 
                  name='Users'),
            row=1, col=1
        )
        
        # Prices
        fig.add_trace(
            go.Bar(x=sides, y=[result['price_a'], result['price_b']], 
                  name='Prices'),
            row=1, col=2
        )
        
        # Network values
        fig.add_trace(
            go.Bar(x=sides, y=[result['network_value_a'], result['network_value_b']], 
                  name='Network Value'),
            row=2, col=1
        )
        
        # Revenue breakdown
        revenue_a = result['price_a'] * result['users_a']
        revenue_b = result['price_b'] * result['users_b']
        
        fig.add_trace(
            go.Bar(x=sides, y=[revenue_a, revenue_b], 
                  name='Revenue'),
            row=2, col=2
        )
        
        fig.update_layout(
            title="Two-Sided Market Analysis",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def analyze_network_tipping(self, network_strength_range, platform1_quality, platform2_quality):
        """
        Analyze tipping points in network competition
        """
        tipping_results = []
        
        for network_strength in network_strength_range:
            result = self.platform_competition(network_strength, platform1_quality, platform2_quality)
            tipping_results.append({
                'network_strength': network_strength,
                'market_share1': result['market_share1'],
                'market_share2': result['market_share2'],
                'winner': 'Platform 1' if result['market_share1'] > 0.5 else 'Platform 2'
            })
        
        return tipping_results 
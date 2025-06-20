"""
Auction Theory Module
Implements various auction mechanisms and analyzes bidding behavior
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class AuctionTheory:
    def __init__(self):
        pass
    
    def first_price_sealed_bid(self, valuations, reserve_price=0):
        """
        First-price sealed-bid auction
        Bidders submit sealed bids, highest bidder wins and pays their bid
        """
        valuations = np.array(valuations)
        n_bidders = len(valuations)
        
        # In symmetric equilibrium, optimal bid = (n-1)/n * valuation
        # This assumes uniform distribution of valuations
        equilibrium_bids = (n_bidders - 1) / n_bidders * valuations
        
        # Apply reserve price constraint
        feasible_bids = equilibrium_bids[equilibrium_bids >= reserve_price]
        feasible_bidders = np.where(equilibrium_bids >= reserve_price)[0]
        
        if len(feasible_bids) == 0:
            return {
                'winner': None,
                'winning_bid': 0,
                'revenue': 0,
                'winner_surplus': 0,
                'efficiency': 0,
                'bids': equilibrium_bids,
                'auction_type': 'First-Price Sealed-Bid'
            }
        
        # Winner is highest bidder
        winner_idx = feasible_bidders[np.argmax(feasible_bids)]
        winning_bid = feasible_bids[np.argmax(feasible_bids)]
        
        # Winner's surplus = valuation - payment
        winner_surplus = valuations[winner_idx] - winning_bid
        
        # Efficiency: did the highest-value bidder win?
        efficiency = 1.0 if winner_idx == np.argmax(valuations) else 0.0
        
        return {
            'winner': winner_idx,
            'winning_bid': winning_bid,
            'revenue': winning_bid,
            'winner_surplus': winner_surplus,
            'efficiency': efficiency,
            'bids': equilibrium_bids,
            'valuations': valuations,
            'auction_type': 'First-Price Sealed-Bid'
        }
    
    def second_price_sealed_bid(self, valuations, reserve_price=0):
        """
        Second-price sealed-bid auction (Vickrey auction)
        Highest bidder wins but pays the second-highest bid
        """
        valuations = np.array(valuations)
        
        # In second-price auction, optimal strategy is to bid your true valuation
        bids = valuations.copy()
        
        # Apply reserve price
        feasible_bidders = np.where(bids >= reserve_price)[0]
        
        if len(feasible_bidders) == 0:
            return {
                'winner': None,
                'winning_bid': 0,
                'revenue': 0,
                'winner_surplus': 0,
                'efficiency': 0,
                'bids': bids,
                'auction_type': 'Second-Price Sealed-Bid'
            }
        
        feasible_bids = bids[feasible_bidders]
        
        # Winner is highest bidder
        winner_idx = feasible_bidders[np.argmax(feasible_bids)]
        
        # Payment is second highest bid (or reserve price if only one bidder)
        if len(feasible_bids) > 1:
            payment = np.partition(feasible_bids, -2)[-2]  # Second highest
        else:
            payment = reserve_price
        
        payment = max(payment, reserve_price)
        
        # Winner's surplus
        winner_surplus = valuations[winner_idx] - payment
        
        # Efficiency: always efficient (highest valuation wins)
        efficiency = 1.0
        
        return {
            'winner': winner_idx,
            'winning_bid': valuations[winner_idx],  # Bid amount
            'payment': payment,  # Actual payment
            'revenue': payment,
            'winner_surplus': winner_surplus,
            'efficiency': efficiency,
            'bids': bids,
            'valuations': valuations,
            'auction_type': 'Second-Price Sealed-Bid'
        }
    
    def english_auction(self, valuations, reserve_price=0, increment=1):
        """
        English (ascending) auction
        Price starts low and increases until only one bidder remains
        """
        valuations = np.array(valuations)
        active_bidders = np.where(valuations >= reserve_price)[0]
        
        if len(active_bidders) == 0:
            return {
                'winner': None,
                'winning_bid': 0,
                'revenue': 0,
                'winner_surplus': 0,
                'efficiency': 0,
                'final_price': reserve_price,
                'auction_type': 'English Auction'
            }
        
        # Simulate ascending price auction
        current_price = reserve_price
        
        while len(active_bidders) > 1:
            # Remove bidders whose valuation is below current price
            active_bidders = active_bidders[valuations[active_bidders] >= current_price + increment]
            current_price += increment
        
        if len(active_bidders) == 0:
            return {
                'winner': None,
                'winning_bid': 0,
                'revenue': 0,
                'winner_surplus': 0,
                'efficiency': 0,
                'final_price': current_price,
                'auction_type': 'English Auction'
            }
        
        winner_idx = active_bidders[0]
        winning_price = current_price - increment  # Last price with multiple bidders
        
        # In English auction, winner pays just above second-highest valuation
        sorted_valuations = np.sort(valuations[valuations >= reserve_price])
        if len(sorted_valuations) > 1:
            payment = sorted_valuations[-2] + increment  # Second highest + increment
        else:
            payment = reserve_price
        
        winner_surplus = valuations[winner_idx] - payment
        
        # Efficiency: always efficient
        efficiency = 1.0
        
        return {
            'winner': winner_idx,
            'winning_bid': valuations[winner_idx],
            'payment': payment,
            'revenue': payment,
            'winner_surplus': winner_surplus,
            'efficiency': efficiency,
            'final_price': payment,
            'valuations': valuations,
            'auction_type': 'English Auction'
        }
    
    def dutch_auction(self, valuations, starting_price=100, decrement=1):
        """
        Dutch (descending) auction
        Price starts high and decreases until someone accepts
        """
        valuations = np.array(valuations)
        current_price = starting_price
        
        # Sort bidders by valuation (highest first)
        sorted_indices = np.argsort(valuations)[::-1]
        
        # Price descends until someone bids
        for bidder_idx in sorted_indices:
            if current_price <= valuations[bidder_idx]:
                # This bidder accepts the current price
                winner_idx = bidder_idx
                winning_price = current_price
                
                winner_surplus = valuations[winner_idx] - winning_price
                
                # Efficiency: depends on who bids first
                efficiency = 1.0 if winner_idx == np.argmax(valuations) else 0.0
                
                return {
                    'winner': winner_idx,
                    'winning_bid': winning_price,
                    'revenue': winning_price,
                    'winner_surplus': winner_surplus,
                    'efficiency': efficiency,
                    'final_price': winning_price,
                    'valuations': valuations,
                    'auction_type': 'Dutch Auction'
                }
            
            current_price -= decrement
        
        # No one bid (price went too low)
        return {
            'winner': None,
            'winning_bid': 0,
            'revenue': 0,
            'winner_surplus': 0,
            'efficiency': 0,
            'final_price': current_price,
            'auction_type': 'Dutch Auction'
        }
    
    def compare_auction_mechanisms(self, valuations, reserve_price=0):
        """
        Compare outcomes across different auction mechanisms
        """
        fp_result = self.first_price_sealed_bid(valuations, reserve_price)
        sp_result = self.second_price_sealed_bid(valuations, reserve_price)
        english_result = self.english_auction(valuations, reserve_price)
        dutch_result = self.dutch_auction(valuations, max(100, max(valuations) + 10))
        
        comparison = {
            'First-Price Sealed-Bid': fp_result,
            'Second-Price Sealed-Bid': sp_result,
            'English Auction': english_result,
            'Dutch Auction': dutch_result
        }
        
        return comparison
    
    def plot_auction_results(self, result, valuations, auction_type):
        """
        Visualize auction results
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Valuations vs Bids', 'Revenue Analysis', 
                           'Efficiency Metrics', 'Bidder Payoffs'),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        n_bidders = len(valuations)
        bidder_names = [f'Bidder {i+1}' for i in range(n_bidders)]
        
        # Valuations vs Bids
        if 'bids' in result:
            fig.add_trace(
                go.Scatter(x=bidder_names, y=valuations, name='Valuations', 
                          mode='markers', marker=dict(size=10, color='blue')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=bidder_names, y=result['bids'], name='Bids', 
                          mode='markers', marker=dict(size=10, color='red')),
                row=1, col=1
            )
        
        # Revenue Analysis
        revenue_data = ['Seller Revenue', 'Winner Surplus']
        revenue_values = [result['revenue'], result['winner_surplus']]
        
        fig.add_trace(
            go.Bar(x=revenue_data, y=revenue_values, name='Revenue/Surplus'),
            row=1, col=2
        )
        
        # Efficiency Metrics
        efficiency_data = ['Efficiency', 'Revenue Efficiency']
        efficiency_values = [result['efficiency'], 
                           result['revenue'] / max(valuations) if max(valuations) > 0 else 0]
        
        fig.add_trace(
            go.Bar(x=efficiency_data, y=efficiency_values, name='Efficiency'),
            row=2, col=1
        )
        
        # Bidder Payoffs
        payoffs = np.zeros(n_bidders)
        if result['winner'] is not None:
            payoffs[result['winner']] = result['winner_surplus']
        
        colors = ['gold' if i == result['winner'] else 'lightblue' for i in range(n_bidders)]
        
        fig.add_trace(
            go.Bar(x=bidder_names, y=payoffs, name='Payoffs', 
                  marker=dict(color=colors)),
            row=2, col=2
        )
        
        fig.update_layout(
            title=f"{auction_type} - Auction Results",
            height=600,
            showlegend=True
        )
        
        return fig
    
    def revenue_equivalence_analysis(self, valuations_distribution='uniform', n_simulations=1000):
        """
        Analyze revenue equivalence theorem through simulation
        """
        revenues_fp = []
        revenues_sp = []
        
        for _ in range(n_simulations):
            if valuations_distribution == 'uniform':
                # Generate random valuations from uniform distribution
                valuations = np.random.uniform(0, 100, 5)
            else:
                # Normal distribution
                valuations = np.maximum(0, np.random.normal(50, 15, 5))
            
            fp_result = self.first_price_sealed_bid(valuations)
            sp_result = self.second_price_sealed_bid(valuations)
            
            revenues_fp.append(fp_result['revenue'])
            revenues_sp.append(sp_result['revenue'])
        
        return {
            'mean_revenue_fp': np.mean(revenues_fp),
            'mean_revenue_sp': np.mean(revenues_sp),
            'std_revenue_fp': np.std(revenues_fp),
            'std_revenue_sp': np.std(revenues_sp),
            'revenues_fp': revenues_fp,
            'revenues_sp': revenues_sp,
            'revenue_difference': np.mean(revenues_fp) - np.mean(revenues_sp)
        }
    
    def optimal_reserve_price(self, valuations, cost=0):
        """
        Calculate optimal reserve price for seller
        """
        # For uniform distribution, optimal reserve price r* = (v_max + c)/2
        # where v_max is maximum possible valuation and c is seller's cost
        
        max_valuation = max(valuations)
        optimal_reserve = (max_valuation + cost) / 2
        
        # Test different reserve prices
        reserve_prices = np.linspace(0, max_valuation, 50)
        expected_revenues = []
        
        for reserve in reserve_prices:
            revenues = []
            for _ in range(100):  # Monte Carlo simulation
                # Randomly select subset of bidders above reserve
                participating_valuations = [v for v in valuations if v >= reserve]
                if len(participating_valuations) >= 2:
                    sp_result = self.second_price_sealed_bid(participating_valuations, reserve)
                    revenues.append(sp_result['revenue'])
                else:
                    revenues.append(reserve if len(participating_valuations) == 1 else 0)
            
            expected_revenues.append(np.mean(revenues))
        
        # Find reserve price that maximizes expected revenue
        optimal_idx = np.argmax(expected_revenues)
        optimal_reserve_empirical = reserve_prices[optimal_idx]
        
        return {
            'theoretical_optimal': optimal_reserve,
            'empirical_optimal': optimal_reserve_empirical,
            'reserve_prices': reserve_prices,
            'expected_revenues': expected_revenues,
            'max_expected_revenue': max(expected_revenues)
        } 
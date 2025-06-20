"""
Game Theory Applications Module
Implements various strategic games in industrial organization
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import itertools

class GameTheory:
    def __init__(self):
        pass
    
    def prisoners_dilemma(self, payoff_matrix):
        """
        Analyze Prisoner's Dilemma game
        payoff_matrix: 2x2 matrix [[CC, CD], [DC, DD]]
        where C = Cooperate, D = Defect
        """
        strategies = ['Cooperate', 'Defect']
        
        # Find Nash equilibria
        equilibria = self.find_nash_equilibria(payoff_matrix, payoff_matrix, strategies, strategies)
        
        # Analyze dominant strategies
        player1_dominant = self.find_dominant_strategy(payoff_matrix, 'row')
        player2_dominant = self.find_dominant_strategy(payoff_matrix, 'column')
        
        return {
            'payoff_matrix': payoff_matrix,
            'strategies': strategies,
            'equilibrium': equilibria,
            'player1_dominant': player1_dominant,
            'player2_dominant': player2_dominant,
            'game_type': 'Prisoners Dilemma'
        }
    
    def entry_game(self, entry_cost, monopoly_profit, duopoly_profit):
        """
        Market entry game
        """
        # Payoff matrix: [Enter, Stay Out] vs [Enter, Stay Out]
        # If both enter: (duopoly_profit - entry_cost, duopoly_profit - entry_cost)
        # If one enters: (monopoly_profit - entry_cost, 0) or (0, monopoly_profit - entry_cost)
        # If neither enters: (0, 0)
        
        payoff_matrix_p1 = [
            [duopoly_profit - entry_cost, monopoly_profit - entry_cost],
            [0, 0]
        ]
        
        payoff_matrix_p2 = [
            [duopoly_profit - entry_cost, 0],
            [monopoly_profit - entry_cost, 0]
        ]
        
        strategies = ['Enter', 'Stay Out']
        equilibria = self.find_nash_equilibria(payoff_matrix_p1, payoff_matrix_p2, strategies, strategies)
        
        return {
            'payoff_matrix_p1': payoff_matrix_p1,
            'payoff_matrix_p2': payoff_matrix_p2,
            'strategies': strategies,
            'equilibrium': equilibria,
            'entry_cost': entry_cost,
            'monopoly_profit': monopoly_profit,
            'duopoly_profit': duopoly_profit,
            'game_type': 'Entry Game'
        }
    
    def pricing_game(self, payoff_matrix):
        """
        Pricing competition game
        """
        strategies = ['High Price', 'Low Price']
        
        # Assuming symmetric game
        equilibria = self.find_nash_equilibria(payoff_matrix, payoff_matrix, strategies, strategies)
        
        return {
            'payoff_matrix': payoff_matrix,
            'strategies': strategies,
            'equilibrium': equilibria,
            'game_type': 'Pricing Game'
        }
    
    def investment_game(self, investment_cost, high_demand_prob, 
                       high_demand_profit, low_demand_profit, no_invest_profit):
        """
        Investment under uncertainty game
        """
        # Expected payoffs
        invest_payoff = (high_demand_prob * high_demand_profit + 
                        (1 - high_demand_prob) * low_demand_profit - investment_cost)
        
        no_invest_payoff = no_invest_profit
        
        # Simple decision analysis
        optimal_strategy = 'Invest' if invest_payoff > no_invest_payoff else 'No Investment'
        
        return {
            'invest_expected_payoff': invest_payoff,
            'no_invest_payoff': no_invest_payoff,
            'optimal_strategy': optimal_strategy,
            'investment_cost': investment_cost,
            'high_demand_prob': high_demand_prob,
            'game_type': 'Investment Game'
        }
    
    def find_nash_equilibria(self, payoff_matrix_p1, payoff_matrix_p2, strategies_p1, strategies_p2):
        """
        Find pure strategy Nash equilibria
        """
        equilibria = []
        n_strategies_p1 = len(strategies_p1)
        n_strategies_p2 = len(strategies_p2)
        
        for i in range(n_strategies_p1):
            for j in range(n_strategies_p2):
                # Check if (i,j) is a Nash equilibrium
                is_nash = True
                
                # Check if player 1 wants to deviate
                current_payoff_p1 = payoff_matrix_p1[i][j]
                for k in range(n_strategies_p1):
                    if payoff_matrix_p1[k][j] > current_payoff_p1:
                        is_nash = False
                        break
                
                # Check if player 2 wants to deviate
                if is_nash:
                    current_payoff_p2 = payoff_matrix_p2[i][j]
                    for l in range(n_strategies_p2):
                        if payoff_matrix_p2[i][l] > current_payoff_p2:
                            is_nash = False
                            break
                
                if is_nash:
                    equilibria.append((strategies_p1[i], strategies_p2[j]))
        
        return equilibria
    
    def find_dominant_strategy(self, payoff_matrix, player):
        """
        Find dominant strategy for a player
        """
        if player == 'row':
            # Compare rows
            if all(payoff_matrix[0][j] > payoff_matrix[1][j] for j in range(len(payoff_matrix[0]))):
                return 'Strategy 1 dominates'
            elif all(payoff_matrix[1][j] > payoff_matrix[0][j] for j in range(len(payoff_matrix[0]))):
                return 'Strategy 2 dominates'
        else:  # column player
            # Compare columns
            if all(payoff_matrix[i][0] > payoff_matrix[i][1] for i in range(len(payoff_matrix))):
                return 'Strategy 1 dominates'
            elif all(payoff_matrix[i][1] > payoff_matrix[i][0] for i in range(len(payoff_matrix))):
                return 'Strategy 2 dominates'
        
        return 'No dominant strategy'
    
    def create_payoff_matrix_display(self, payoff_matrix, row_strategies, col_strategies):
        """
        Create a formatted payoff matrix for display
        """
        # Create DataFrame for better display
        matrix_data = []
        for i, row_strategy in enumerate(row_strategies):
            row_data = [row_strategy]
            for j, col_strategy in enumerate(col_strategies):
                row_data.append(f"{payoff_matrix[i][j]}")
            matrix_data.append(row_data)
        
        columns = ['Player 1 \\ Player 2'] + col_strategies
        df = pd.DataFrame(matrix_data, columns=columns)
        
        return df
    
    def repeated_game_simulation(self, payoff_matrix, strategies, n_rounds=100, 
                                strategy_p1='tit_for_tat', strategy_p2='always_defect'):
        """
        Simulate repeated game with different strategies
        """
        # Initialize
        history_p1 = []
        history_p2 = []
        payoffs_p1 = []
        payoffs_p2 = []
        
        # First round - cooperate for tit-for-tat
        if strategy_p1 == 'tit_for_tat':
            action_p1 = 0  # Cooperate
        else:
            action_p1 = 1  # Defect
        
        if strategy_p2 == 'always_cooperate':
            action_p2 = 0  # Cooperate
        else:
            action_p2 = 1  # Defect
        
        for round_num in range(n_rounds):
            # Record actions
            history_p1.append(action_p1)
            history_p2.append(action_p2)
            
            # Calculate payoffs
            payoff_p1 = payoff_matrix[action_p1][action_p2]
            payoff_p2 = payoff_matrix[action_p2][action_p1]  # Symmetric game
            
            payoffs_p1.append(payoff_p1)
            payoffs_p2.append(payoff_p2)
            
            # Determine next actions based on strategies
            if round_num < n_rounds - 1:  # Not last round
                if strategy_p1 == 'tit_for_tat':
                    action_p1 = action_p2  # Copy opponent's last move
                elif strategy_p1 == 'always_cooperate':
                    action_p1 = 0
                else:  # always_defect
                    action_p1 = 1
                
                if strategy_p2 == 'tit_for_tat':
                    action_p2 = action_p1  # Copy opponent's last move
                elif strategy_p2 == 'always_cooperate':
                    action_p2 = 0
                else:  # always_defect
                    action_p2 = 1
        
        return {
            'history_p1': history_p1,
            'history_p2': history_p2,
            'payoffs_p1': payoffs_p1,
            'payoffs_p2': payoffs_p2,
            'total_payoff_p1': sum(payoffs_p1),
            'total_payoff_p2': sum(payoffs_p2),
            'cooperation_rate_p1': history_p1.count(0) / len(history_p1),
            'cooperation_rate_p2': history_p2.count(0) / len(history_p2)
        }
    
    def plot_game_analysis(self, result):
        """
        Visualize game theory results
        """
        if result['game_type'] == 'Prisoners Dilemma':
            return self._plot_prisoners_dilemma(result)
        elif result['game_type'] == 'Entry Game':
            return self._plot_entry_game(result)
        else:
            return self._plot_general_game(result)
    
    def _plot_prisoners_dilemma(self, result):
        """Plot Prisoner's Dilemma analysis"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Payoff Matrix', 'Strategy Analysis'),
            specs=[[{"type": "table"}, {"type": "bar"}]]
        )
        
        # Payoff matrix as heatmap
        matrix = result['payoff_matrix']
        strategies = result['strategies']
        
        # Strategy analysis
        analysis_data = []
        if result['equilibrium']:
            for eq in result['equilibrium']:
                analysis_data.append(f"{eq[0]} vs {eq[1]}")
        
        fig.add_trace(
            go.Bar(x=['Nash Equilibria'], y=[len(result['equilibrium'])], 
                  text=analysis_data, textposition='auto'),
            row=1, col=2
        )
        
        fig.update_layout(
            title="Prisoner's Dilemma Analysis",
            height=400
        )
        
        return fig
    
    def _plot_entry_game(self, result):
        """Plot Entry Game analysis"""
        fig = go.Figure()
        
        # Create decision tree visualization
        # This is a simplified representation
        strategies = ['Enter', 'Stay Out']
        firms = ['Firm 1', 'Firm 2']
        
        # Plot as decision matrix
        for i, strategy1 in enumerate(strategies):
            for j, strategy2 in enumerate(strategies):
                payoff1 = result['payoff_matrix_p1'][i][j]
                payoff2 = result['payoff_matrix_p2'][i][j]
                
                fig.add_trace(go.Scatter(
                    x=[i], y=[j],
                    mode='markers+text',
                    marker=dict(size=50, color=payoff1+payoff2, colorscale='Viridis'),
                    text=f"({payoff1:.1f}, {payoff2:.1f})",
                    textposition="middle center",
                    name=f"{strategy1} vs {strategy2}"
                ))
        
        fig.update_layout(
            title="Entry Game Payoff Matrix",
            xaxis=dict(tickvals=[0, 1], ticktext=strategies, title="Firm 1 Strategy"),
            yaxis=dict(tickvals=[0, 1], ticktext=strategies, title="Firm 2 Strategy"),
            height=500
        )
        
        return fig
    
    def _plot_general_game(self, result):
        """Plot general game results"""
        # Simple bar chart of strategies
        fig = go.Figure()
        
        strategies = result.get('strategies', ['Strategy 1', 'Strategy 2'])
        equilibria_count = len(result.get('equilibrium', []))
        
        fig.add_trace(go.Bar(
            x=['Number of Equilibria'],
            y=[equilibria_count],
            text=[f"{equilibria_count} equilibria found"],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f"{result['game_type']} Analysis",
            height=400
        )
        
        return fig 
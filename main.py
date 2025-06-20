"""
Energy Economics Simulation Suite
Main application entry point with Streamlit interface
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import energy economics modules
from modules.electricity_markets import ElectricityMarkets
from modules.renewable_energy import RenewableEnergy
from modules.energy_pricing import EnergyPricing
from modules.carbon_markets import CarbonMarkets
from modules.grid_operations import GridOperations
from modules.energy_policy import EnergyPolicy

# Configure page
st.set_page_config(
    page_title="Energy Economics Simulation Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("⚡ Energy Economics Simulation Suite")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("🔋 Energy Economics Modules")
    module = st.sidebar.selectbox(
        "Choose a module:",
        [
            "Electricity Market Design",
            "Renewable Energy Economics", 
            "Energy Pricing & Demand",
            "Carbon Markets & Trading",
            "Grid Operations & Storage",
            "Energy Policy Analysis"
        ]
    )
    
    # Module routing
    if module == "Electricity Market Design":
        electricity_markets_page()
    elif module == "Renewable Energy Economics":
        renewable_energy_page()
    elif module == "Energy Pricing & Demand":
        energy_pricing_page()
    elif module == "Carbon Markets & Trading":
        carbon_markets_page()
    elif module == "Grid Operations & Storage":
        grid_operations_page()
    elif module == "Energy Policy Analysis":
        energy_policy_page()

def electricity_markets_page():
    st.header("⚡ Electricity Market Design")
    market_sim = ElectricityMarkets()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Market Parameters")
        market_type = st.selectbox("Market Structure", 
            ["Perfect Competition", "Monopoly", "Oligopoly", "Nodal Pricing"])
        
        # Demand parameters
        peak_demand = st.slider("Peak Demand (GW)", 50, 200, 100)
        demand_elasticity = st.slider("Demand Elasticity", -2.0, -0.1, -0.5, 0.1)
        load_factor = st.slider("Load Factor", 0.4, 0.9, 0.7, 0.05)
        
        # Supply parameters
        coal_capacity = st.slider("Coal Capacity (GW)", 0, 100, 40)
        gas_capacity = st.slider("Gas Capacity (GW)", 0, 100, 30)
        renewable_capacity = st.slider("Renewable Capacity (GW)", 0, 100, 20)
        
        # Cost parameters
        coal_cost = st.slider("Coal Marginal Cost ($/MWh)", 20, 80, 40)
        gas_cost = st.slider("Gas Marginal Cost ($/MWh)", 30, 120, 60)
        renewable_cost = st.slider("Renewable Marginal Cost ($/MWh)", 0, 50, 10)
    
    with col2:
        st.subheader("Market Analysis")
        
        # Create supply and demand data
        supply_data = {
            'coal': {'capacity': coal_capacity, 'cost': coal_cost},
            'gas': {'capacity': gas_capacity, 'cost': gas_cost},
            'renewable': {'capacity': renewable_capacity, 'cost': renewable_cost}
        }
        
        demand_data = {
            'peak_demand': peak_demand,
            'elasticity': demand_elasticity,
            'load_factor': load_factor
        }
        
        if market_type == "Perfect Competition":
            result = market_sim.perfect_competition_market(supply_data, demand_data)
        elif market_type == "Monopoly":
            result = market_sim.monopoly_market(supply_data, demand_data)
        elif market_type == "Oligopoly":
            result = market_sim.oligopoly_market(supply_data, demand_data)
        else:  # Nodal Pricing
            result = market_sim.nodal_pricing_market(supply_data, demand_data)
        
        # Display results
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Clearing Price", f"${result['price']:.2f}/MWh")
            st.metric("Total Generation", f"{result['quantity']:.1f} GW")
        with col_b:
            st.metric("Consumer Surplus", f"${result['consumer_surplus']:.1f}M")
            st.metric("Producer Surplus", f"${result['producer_surplus']:.1f}M")
        with col_c:
            st.metric("Market Efficiency", f"{result['efficiency']:.1%}")
            st.metric("Carbon Intensity", f"{result['carbon_intensity']:.1f} kg/MWh")
        
        # Plot market results
        fig = market_sim.plot_market_results(result, supply_data, demand_data)
        st.plotly_chart(fig, use_container_width=True)

def renewable_energy_page():
    st.header("🌱 Renewable Energy Economics")
    renewable_sim = RenewableEnergy()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Technology Parameters")
        technology = st.selectbox("Renewable Technology", 
            ["Solar PV", "Wind Onshore", "Wind Offshore", "Hydroelectric"])
        
        # Cost parameters
        capex = st.slider("Capital Cost ($/kW)", 500, 5000, 1500)
        opex = st.slider("Operating Cost ($/kW/year)", 10, 100, 40)
        capacity_factor = st.slider("Capacity Factor", 0.1, 0.9, 0.35, 0.05)
        lifetime = st.slider("Project Lifetime (years)", 15, 30, 25)
        
        # Financial parameters
        discount_rate = st.slider("Discount Rate (%)", 2, 15, 8, 1)
        tax_credit = st.slider("Tax Credit (%)", 0, 50, 30, 5)
        
        # Market parameters
        electricity_price = st.slider("Electricity Price ($/MWh)", 30, 150, 70)
        learning_rate = st.slider("Technology Learning Rate (%)", 5, 25, 15, 1)
    
    with col2:
        st.subheader("Economic Analysis")
        
        # Calculate LCOE and other metrics
        result = renewable_sim.calculate_lcoe(
            capex, opex, capacity_factor, lifetime, 
            discount_rate/100, tax_credit/100
        )
        
        # Competitiveness analysis
        competitiveness = renewable_sim.competitiveness_analysis(
            result['lcoe'], electricity_price, learning_rate/100
        )
        
        # Learning curve projection
        learning_curve = renewable_sim.learning_curve_projection(
            capex, learning_rate/100, years=20
        )
        
        # Display metrics
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("LCOE", f"${result['lcoe']:.2f}/MWh")
            st.metric("Capacity Factor", f"{capacity_factor:.1%}")
        with col_b:
            st.metric("NPV", f"${result['npv']:.1f}M")
            st.metric("IRR", f"{result['irr']:.1%}")
        with col_c:
            st.metric("Payback Period", f"{result['payback']:.1f} years")
            st.metric("Grid Parity", "✅" if result['lcoe'] < electricity_price else "❌")
        
        # Plot analysis
        fig = renewable_sim.plot_renewable_analysis(result, competitiveness, learning_curve)
        st.plotly_chart(fig, use_container_width=True)

def energy_pricing_page():
    st.header("💰 Energy Pricing & Demand")
    pricing_sim = EnergyPricing()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Pricing Structure")
        pricing_type = st.selectbox("Pricing Mechanism", 
            ["Time-of-Use", "Real-Time Pricing", "Tiered Pricing", "Peak Load Pricing"])
        
        # Demand parameters
        base_demand = st.slider("Base Load (GW)", 20, 100, 50)
        peak_multiplier = st.slider("Peak/Base Ratio", 1.2, 3.0, 1.8, 0.1)
        price_elasticity = st.slider("Price Elasticity", -2.0, -0.1, -0.3, 0.1)
        
        # Cost parameters
        base_cost = st.slider("Base Generation Cost ($/MWh)", 20, 60, 35)
        peak_cost = st.slider("Peak Generation Cost ($/MWh)", 50, 200, 100)
        transmission_cost = st.slider("Transmission Cost ($/MWh)", 5, 25, 10)
        
        # Policy parameters
        carbon_price = st.slider("Carbon Price ($/tonne)", 0, 100, 25)
        renewable_mandate = st.slider("Renewable Mandate (%)", 0, 50, 20, 5)
    
    with col2:
        st.subheader("Pricing Analysis")
        
        pricing_data = {
            'base_demand': base_demand,
            'peak_multiplier': peak_multiplier,
            'elasticity': price_elasticity,
            'base_cost': base_cost,
            'peak_cost': peak_cost,
            'transmission_cost': transmission_cost,
            'carbon_price': carbon_price,
            'renewable_mandate': renewable_mandate/100
        }
        
        if pricing_type == "Time-of-Use":
            result = pricing_sim.time_of_use_pricing(pricing_data)
        elif pricing_type == "Real-Time Pricing":
            result = pricing_sim.real_time_pricing(pricing_data)
        elif pricing_type == "Tiered Pricing":
            result = pricing_sim.tiered_pricing(pricing_data)
        else:  # Peak Load Pricing
            result = pricing_sim.peak_load_pricing(pricing_data)
        
        # Display results
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Average Price", f"${result['avg_price']:.2f}/MWh")
            st.metric("Peak Price", f"${result['peak_price']:.2f}/MWh")
        with col_b:
            st.metric("Load Factor", f"{result['load_factor']:.2%}")
            st.metric("Peak Demand", f"{result['peak_demand']:.1f} GW")
        with col_c:
            st.metric("Revenue", f"${result['revenue']:.1f}M")
            st.metric("Consumer Surplus", f"${result['consumer_surplus']:.1f}M")
        
        # Plot pricing analysis
        fig = pricing_sim.plot_pricing_analysis(result, pricing_type)
        st.plotly_chart(fig, use_container_width=True)

def carbon_markets_page():
    st.header("🌍 Carbon Markets & Trading")
    carbon_sim = CarbonMarkets()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Carbon Market Design")
        market_design = st.selectbox("Market Type", 
            ["Cap-and-Trade", "Carbon Tax", "Hybrid System", "Offset Markets"])
        
        # Emission parameters
        total_emissions = st.slider("Total Emissions (Mt CO2)", 100, 1000, 500)
        emission_cap = st.slider("Emission Cap (Mt CO2)", 50, 800, 400)
        reduction_target = st.slider("Reduction Target (%)", 10, 80, 30, 5)
        
        # Cost parameters
        abatement_cost = st.slider("Marginal Abatement Cost ($/tonne)", 20, 200, 80)
        monitoring_cost = st.slider("Monitoring Cost ($/tonne)", 1, 20, 5)
        transaction_cost = st.slider("Transaction Cost (%)", 0.5, 10.0, 2.0, 0.5)
        
        # Market parameters
        price_volatility = st.slider("Price Volatility (%)", 5, 50, 20, 5)
        banking_allowed = st.checkbox("Banking Allowed", value=True)
        offset_ratio = st.slider("Offset Ratio", 0.5, 2.0, 1.0, 0.1)
    
    with col2:
        st.subheader("Carbon Market Analysis")
        
        market_data = {
            'total_emissions': total_emissions,
            'emission_cap': emission_cap,
            'reduction_target': reduction_target/100,
            'abatement_cost': abatement_cost,
            'monitoring_cost': monitoring_cost,
            'transaction_cost': transaction_cost/100,
            'volatility': price_volatility/100,
            'banking': banking_allowed,
            'offset_ratio': offset_ratio
        }
        
        if market_design == "Cap-and-Trade":
            result = carbon_sim.cap_and_trade_system(market_data)
        elif market_design == "Carbon Tax":
            result = carbon_sim.carbon_tax_system(market_data)
        elif market_design == "Hybrid System":
            result = carbon_sim.hybrid_system(market_data)
        else:  # Offset Markets
            result = carbon_sim.offset_markets(market_data)
        
        # Display results
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Carbon Price", f"${result['carbon_price']:.2f}/tonne")
            st.metric("Emission Reduction", f"{result['emission_reduction']:.1%}")
        with col_b:
            st.metric("Compliance Cost", f"${result['compliance_cost']:.1f}M")
            st.metric("Market Efficiency", f"{result['efficiency']:.1%}")
        with col_c:
            st.metric("Revenue Generated", f"${result['revenue']:.1f}M")
            st.metric("Economic Impact", f"${result['economic_impact']:.1f}M")
        
        # Plot carbon market analysis
        fig = carbon_sim.plot_carbon_market_analysis(result, market_design)
        st.plotly_chart(fig, use_container_width=True)

def grid_operations_page():
    st.header("🔌 Grid Operations & Storage")
    grid_sim = GridOperations()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Grid Configuration")
        grid_type = st.selectbox("Analysis Type", 
            ["Load Balancing", "Storage Optimization", "Grid Stability", "Transmission Planning"])
        
        # Grid parameters
        base_load = st.slider("Base Load (GW)", 30, 150, 80)
        renewable_penetration = st.slider("Renewable Penetration (%)", 10, 80, 40, 5)
        storage_capacity = st.slider("Storage Capacity (GWh)", 0, 100, 20)
        transmission_capacity = st.slider("Transmission Capacity (GW)", 50, 200, 120)
        
        # Reliability parameters
        target_reliability = st.slider("Target Reliability (%)", 95.0, 99.9, 99.5, 0.1)
        reserve_margin = st.slider("Reserve Margin (%)", 10, 30, 15, 1)
        
        # Economic parameters
        storage_cost = st.slider("Storage Cost ($/kWh)", 100, 1000, 300)
        transmission_cost = st.slider("Transmission Cost ($/MW-km)", 500, 2000, 1000)
        outage_cost = st.slider("Outage Cost ($/MWh)", 1000, 10000, 5000, 500)
    
    with col2:
        st.subheader("Grid Analysis")
        
        grid_data = {
            'base_load': base_load,
            'renewable_penetration': renewable_penetration/100,
            'storage_capacity': storage_capacity,
            'transmission_capacity': transmission_capacity,
            'target_reliability': target_reliability/100,
            'reserve_margin': reserve_margin/100,
            'storage_cost': storage_cost,
            'transmission_cost': transmission_cost,
            'outage_cost': outage_cost
        }
        
        if grid_type == "Load Balancing":
            result = grid_sim.load_balancing_analysis(grid_data)
        elif grid_type == "Storage Optimization":
            result = grid_sim.storage_optimization(grid_data)
        elif grid_type == "Grid Stability":
            result = grid_sim.grid_stability_analysis(grid_data)
        else:  # Transmission Planning
            result = grid_sim.transmission_planning(grid_data)
        
        # Display results
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Grid Reliability", f"{result['reliability']:.2%}")
            st.metric("Load Factor", f"{result['load_factor']:.2%}")
        with col_b:
            st.metric("Storage Utilization", f"{result['storage_utilization']:.1%}")
            st.metric("Transmission Utilization", f"{result['transmission_utilization']:.1%}")
        with col_c:
            st.metric("Total Cost", f"${result['total_cost']:.1f}M")
            st.metric("Cost per MWh", f"${result['cost_per_mwh']:.2f}")
        
        # Plot grid analysis
        fig = grid_sim.plot_grid_analysis(result, grid_type)
        st.plotly_chart(fig, use_container_width=True)

def energy_policy_page():
    st.header("📊 Energy Policy Analysis")
    policy_sim = EnergyPolicy()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Policy Parameters")
        policy_type = st.selectbox("Policy Instrument", 
            ["Renewable Portfolio Standard", "Feed-in Tariff", "Energy Efficiency", "Fuel Standards"])
        
        # Policy design parameters
        target_percentage = st.slider("Policy Target (%)", 10, 80, 30, 5)
        implementation_period = st.slider("Implementation Period (years)", 5, 20, 10)
        penalty_rate = st.slider("Non-compliance Penalty ($/MWh)", 10, 100, 50)
        
        # Economic parameters
        policy_cost = st.slider("Policy Administration Cost ($M)", 10, 500, 100)
        consumer_burden = st.slider("Consumer Cost Share (%)", 20, 100, 70, 10)
        innovation_effect = st.slider("Innovation Stimulus (%)", 0, 50, 15, 5)
        
        # Environmental parameters
        emission_factor = st.slider("Emission Factor (kg CO2/MWh)", 200, 1000, 600)
        health_benefits = st.slider("Health Benefits ($/tonne CO2)", 50, 300, 150)
        environmental_value = st.slider("Environmental Value ($/tonne CO2)", 25, 150, 75)
    
    with col2:
        st.subheader("Policy Impact Analysis")
        
        policy_data = {
            'target_percentage': target_percentage/100,
            'implementation_period': implementation_period,
            'penalty_rate': penalty_rate,
            'policy_cost': policy_cost,
            'consumer_burden': consumer_burden/100,
            'innovation_effect': innovation_effect/100,
            'emission_factor': emission_factor,
            'health_benefits': health_benefits,
            'environmental_value': environmental_value
        }
        
        if policy_type == "Renewable Portfolio Standard":
            result = policy_sim.renewable_portfolio_standard(policy_data)
        elif policy_type == "Feed-in Tariff":
            result = policy_sim.feed_in_tariff(policy_data)
        elif policy_type == "Energy Efficiency":
            result = policy_sim.energy_efficiency_standard(policy_data)
        else:  # Fuel Standards
            result = policy_sim.fuel_standards(policy_data)
        
        # Display results
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Policy Effectiveness", f"{result['effectiveness']:.1%}")
            st.metric("Compliance Rate", f"{result['compliance_rate']:.1%}")
        with col_b:
            st.metric("Economic Impact", f"${result['economic_impact']:.1f}M")
            st.metric("Consumer Cost", f"${result['consumer_cost']:.1f}M")
        with col_c:
            st.metric("Environmental Benefit", f"${result['environmental_benefit']:.1f}M")
            st.metric("Net Social Benefit", f"${result['net_benefit']:.1f}M")
        
        # Plot policy analysis
        fig = policy_sim.plot_policy_analysis(result, policy_type)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main() 
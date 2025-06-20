# Industrial Organization Economics Simulation Suite

A comprehensive interactive simulation platform for exploring key concepts in Industrial Organization Economics. This project provides hands-on analysis tools for market structures, competition models, game theory, product differentiation, auction mechanisms, and network effects.

## 🎯 Features

### 1. Market Structure Analysis
- **Perfect Competition**: Analyze efficient market outcomes with price-taking behavior
- **Monopoly**: Explore market power, deadweight loss, and welfare implications
- **Oligopoly**: Cournot competition with multiple firms
- **Monopolistic Competition**: Differentiated products with free entry

### 2. Price Competition Models
- **Bertrand Competition**: Price competition with product differentiation
- **Cournot Competition**: Quantity competition with strategic interaction
- **Stackelberg Competition**: Sequential move advantage in quantity setting

### 3. Game Theory Applications
- **Prisoner's Dilemma**: Classic cooperation vs. defection analysis
- **Entry Games**: Strategic market entry decisions
- **Pricing Games**: Coordination problems in price setting
- **Investment Games**: Decision-making under uncertainty

### 4. Product Differentiation
- **Hotelling's Linear City**: Spatial competition and location choice
- **Circular City Model**: Competition around a circle (Salop model)
- **Vertical Differentiation**: Quality competition and market segmentation

### 5. Auction Theory
- **First-Price Sealed-Bid**: Strategic bidding below valuation
- **Second-Price Sealed-Bid**: Truth-telling Vickrey auctions
- **English Auctions**: Ascending price mechanisms
- **Dutch Auctions**: Descending price mechanisms

### 6. Network Effects
- **Platform Competition**: Two-sided markets with network externalities
- **Adoption Dynamics**: Critical mass and tipping points
- **Network Externalities**: Welfare analysis of network goods

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download the project files
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Launch the interactive web interface:
```bash
streamlit run main.py
```

The application will open in your web browser at `http://localhost:8501`

## 💡 How to Use

1. **Select a Module**: Use the sidebar to choose from the 6 main simulation areas
2. **Adjust Parameters**: Modify economic parameters using the intuitive sliders and inputs
3. **Analyze Results**: View real-time calculations and interactive visualizations
4. **Compare Scenarios**: Experiment with different parameter values to understand economic relationships

## 📊 Key Simulations

### Market Power Analysis
Compare outcomes across different market structures:
- Consumer and producer surplus
- Deadweight loss calculations
- Efficiency metrics

### Strategic Interaction
Explore game theory concepts:
- Nash equilibrium identification
- Dominant strategy analysis
- Repeated game dynamics

### Auction Design
Analyze different auction mechanisms:
- Revenue equivalence
- Efficiency comparisons
- Optimal bidding strategies

### Network Economics
Study network effects and platform competition:
- Adoption curves and critical mass
- Two-sided market pricing
- Winner-take-all dynamics

## 🔧 Technical Implementation

### Architecture
- **Frontend**: Streamlit interactive web interface
- **Backend**: Python simulation engines for each economic model
- **Visualization**: Plotly for interactive charts and graphs
- **Computation**: NumPy and SciPy for numerical analysis

### Module Structure
```
modules/
├── market_structures.py      # Market structure analysis
├── price_competition.py      # Competition models
├── game_theory.py           # Strategic games
├── product_differentiation.py # Spatial and vertical differentiation
├── auction_theory.py        # Auction mechanisms
└── network_effects.py       # Network externalities
```

## 📚 Educational Applications

### For Students
- Visualize abstract economic concepts
- Experiment with parameter changes
- Understand equilibrium analysis
- Explore welfare implications

### For Instructors
- Interactive lecture demonstrations
- Assignment and project material
- Comparative static analysis
- Real-time scenario testing

### For Researchers
- Model validation and testing
- Parameter sensitivity analysis
- Scenario comparison tools
- Publication-ready visualizations

## 🎓 Learning Objectives

After using this simulation suite, users will understand:

1. **Market Structure Effects**: How market concentration affects prices, quantities, and welfare
2. **Strategic Behavior**: Game theory applications in industrial organization
3. **Competition Policy**: Welfare effects of different competitive environments
4. **Product Strategy**: Differentiation and positioning decisions
5. **Auction Design**: Mechanism design for optimal outcomes
6. **Network Economics**: Platform competition and network externalities

## 🤝 Contributing

This is an educational project designed for learning and teaching industrial organization economics. Contributions, suggestions, and feedback are welcome!

## 📄 License

This project is designed for educational use. Please cite appropriately if used in academic work.

## 🔗 References

- Tirole, J. (1988). *The Theory of Industrial Organization*
- Cabral, L. (2017). *Introduction to Industrial Organization*
- Belleflamme, P. & Peitz, M. (2015). *Industrial Organization: Markets and Strategies*

## 💬 Support

For questions or issues with the simulation:
1. Check the parameter tooltips in the interface
2. Review the economic theory behind each model
3. Experiment with different parameter combinations

---

*Built with ❤️ for economics education* 
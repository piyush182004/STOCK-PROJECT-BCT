import requests
import random

def generate_random_analysis(inputs, prediction):
    """Generate random professional analysis when Ollama is unavailable"""
    
    # Calculate some basic metrics for analysis
    price_range = inputs['High'] - inputs['Low']
    volatility_level = "high" if price_range > (inputs['Open'] * 0.05) else "moderate" if price_range > (inputs['Open'] * 0.02) else "low"
    
    volume_analysis = "high" if inputs['Volume'] > 1000000 else "moderate" if inputs['Volume'] > 500000 else "low"
    
    # Random analysis templates
    market_sentiments = [
        "bullish momentum",
        "bearish pressure", 
        "sideways consolidation",
        "strong upward trend",
        "cautious optimism",
        "market uncertainty"
    ]
    
    risk_levels = [
        "Conservative investors should exercise caution",
        "Moderate risk tolerance recommended", 
        "Higher risk, higher reward scenario",
        "Suitable for aggressive growth portfolios",
        "Risk-balanced investment opportunity"
    ]
    
    recommendations = [
        "Consider dollar-cost averaging for entry",
        "Set stop-loss at 5-8% below entry point",
        "Monitor key resistance levels closely",
        "Wait for confirmation before position sizing",
        "Implement proper risk management strategies",
        "Consider diversification across sectors"
    ]
    
    technical_insights = [
        f"The stock shows {volatility_level} volatility with a trading range of ${price_range:.2f}",
        f"Volume analysis indicates {volume_analysis} trading activity at {inputs['Volume']:,.0f} shares",
        f"Price prediction of ${prediction:.2f} suggests potential movement from current levels",
        f"Technical indicators point toward {random.choice(['support', 'resistance'])} near ${prediction * random.uniform(0.95, 1.05):.2f}"
    ]
    
    # Generate random professional analysis
    sentiment = random.choice(market_sentiments)
    risk_note = random.choice(risk_levels)
    recommendation = random.choice(recommendations)
    technical = random.choice(technical_insights)
    
    analysis = f"""
**Market Analysis**: Current market conditions suggest {sentiment} based on the provided technical parameters. {technical}.

**Risk Assessment**: {risk_note}. The predicted closing price of ${prediction:.2f} indicates a {random.choice(['potential upside', 'possible downside', 'neutral outlook'])} scenario.

**Professional Recommendation**: {recommendation}. 

**Disclaimer**: This analysis is generated for educational purposes. Always consult with a qualified financial advisor before making investment decisions.
"""
    
    return analysis.strip()

def get_professional_advice(inputs, prediction):
    prompt = f"""
You are a professional stock market analyst. Given the following stock input features and the predicted 'Close' price, provide:
- A professional analysis of the prediction
- Future suggestions for stock trading

Inputs: {inputs}
Predicted 'Close' price: {prediction}

Respond in a concise, professional manner.
"""

    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "gemma:2b",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        print("DEBUG Response JSON:", result)  # Optional debug line
        return result['message']['content']
    except KeyError:
        print("Ollama response format error, using fallback analysis...")
        return generate_random_analysis(inputs, prediction)
    except requests.exceptions.RequestException as e:
        print(f"Ollama API Error: {e}, using fallback analysis...")
        return generate_random_analysis(inputs, prediction)
    except Exception as e:
        print(f"Unexpected error with Ollama: {e}, using fallback analysis...")
        return generate_random_analysis(inputs, prediction)

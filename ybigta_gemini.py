# -*- coding: utf-8 -*-
# pip install "google-cloud-aiplatform>=1.38"


import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from typing import List, Dict

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/shgla/OneDrive/ybigta/ybigta-414314-a438fffa0b91.json"

project_id = "ybigta-414314"
location = "asia-northeast3"  # 한국 서울

vertexai.init(project=project_id, location=location)

model = GenerativeModel("gemini-pro")


def summarize(news_article: str) -> str:
    """
    Summarizes a financial news article using the GenerativeModel.

    Parameters:
    - news_article (str): The financial news article to be summarized.

    Returns:
    - str: The summary of the financial news article.
    """

    # Generate content
    responses = model.generate_content(
        f"""Provide a brief summary for the following article:

        Example 1
        Input:
        Emerging markets soared more than 33 percent in 2017, and Todd Gordon of TradingAnalysis.com says the rally won't stop. A big part of the rally in emerging markets, tracked by the emerging market ETF EEM , was a weak dollar. And given that Gordon still sees the inverse relationship between EEM and the dollar, measured in his charts by the dollar-tracking ETF UUP , he believes the U.S. currency will continue to help the group. "We have a falling U.S. dollar, which will support international and emerging market currencies and will give those EEM stocks a boost," Gordon said Tuesday on CNBC's "Trading Nation." The U.S. dollar in 2017 posted its worst annual performance in 14 years, while EEM saw its best performance since 2013. As for how high the latter could go, Gordon says EEM has broken "resistance" at around $45, which was the ETF's 2014 highs. That $45 region is now what he calls "support," and he sees it rallying to $50, which the ETF hasn't hit since mid-2011. To play for a move higher, Gordon suggested buying the February 48/50 call spread for 72 cents, or $72 per options contract. This means that if EEM closes above $50 on Feb. 16, then Gordon could make a maximum reward of $128 on the trade. But if EEM were to close below $48, then Gordon would lose the $72 he paid for the trade. As a result, Gordon wants to establish a point at which to get out. "If the 72 cent premium we just laid out gets cut in half to about 36 cents, let's cut the trade and move on," he said. EEM started the year off strong, rallying more than 1 percent on Tuesday.

        Output:
        ###
        The article discusses the strong performance of emerging markets in 2017, with a focus on the role of a weak U.S. dollar in driving the rally. Todd Gordon of TradingAnalysis.com suggests that the inverse relationship between the emerging market ETF (EEM) and the U.S. dollar (measured by the UUP ETF) will continue to benefit international and emerging market currencies. Gordon predicts a potential rise in EEM, citing a breakthrough in resistance at $45 and anticipates a rally to $50. He recommends an options trading strategy and sets conditions for exiting the trade. The article also mentions EEM's strong start in the current year, rallying over 1 percent on a specific day.

        Input:
        {news_article}

        Output:
        ###
        """,

        generation_config={
            "max_output_tokens": 200,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        # stream=True,
    )

    return responses.text


def detect_economic_terms(news_article: str) -> List[str]:
    """
    Tries to detect economic terms in a financial news article using the GenerativeModel.

    Parameters:
    - news_article (str): The financial news article to be analyzed.

    Returns:
    - List[str]: List of detected economic terms.
    """

    # Build a prompt for economic term detection
    prompt = f"""Identify economic terms in the following financial news article.
                Input:
                Emerging markets soared more than 33 percent in 2017, and Todd Gordon of TradingAnalysis.com says the rally won't stop. A big part of the rally in emerging markets, tracked by the emerging market ETF EEM , was a weak dollar. And given that Gordon still sees the inverse relationship between EEM and the dollar, measured in his charts by the dollar-tracking ETF UUP , he believes the U.S. currency will continue to help the group. "We have a falling U.S. dollar, which will support international and emerging market currencies and will give those EEM stocks a boost," Gordon said Tuesday on CNBC's "Trading Nation." The U.S. dollar in 2017 posted its worst annual performance in 14 years, while EEM saw its best performance since 2013. As for how high the latter could go, Gordon says EEM has broken "resistance" at around $45, which was the ETF's 2014 highs. That $45 region is now what he calls "support," and he sees it rallying to $50, which the ETF hasn't hit since mid-2011. To play for a move higher, Gordon suggested buying the February 48/50 call spread for 72 cents, or $72 per options contract. This means that if EEM closes above $50 on Feb. 16, then Gordon could make a maximum reward of $128 on the trade. But if EEM were to close below $48, then Gordon would lose the $72 he paid for the trade. As a result, Gordon wants to establish a point at which to get out. "If the 72 cent premium we just laid out gets cut in half to about 36 cents, let's cut the trade and move on," he said. EEM started the year off strong, rallying more than 1 percent on Tuesday.

                Output:
                ###
                Emerging Markets
                ETF (Exchange-Traded Fund)
                Rally
                Weak Dollar
                Inverse Relationship
                Currency
                Resistance and Support
                Options Contract
                Premium
                Maximum Reward
                Move Higher
                Call Spread
                Point of Exit
                Dollar-tracking ETF (UUP)
                Performance
                Annual Performance
                Point
                Resistance Broken
                February 48/50 Call Spread
                Cut the Trade

                Input:
                {news_article}

                Output:
                ###
                """

    # Generate content
    generated_content = model.generate_content(prompt).text

    # Extract economic terms (simple example, may not be accurate)
    economic_terms = [term.strip() for term in generated_content.split('\n')]

    return economic_terms


def get_economic_term_definitions(news_article: str, summary: str, economic_terms: List[str]) -> List[str]:
    """
    Gets definitions for given economic terms using a GenerativeModel.
    Definitions are generated based on the context of the input news article.

    Parameters:
    - news_article (str): The financial news article.
    - summary (str): The summary of the financial news article.
    - economic_terms (List[str]): List of economic terms.

    Returns:
    - List[str]: List of definitions for each economic term.
    """

    economic_terms_string = '\n'.join(economic_terms)

    # Build a prompt for definitions of multiple economic terms
    prompt = f"""Define the following economic terms.
                Definitions should be based on the context of the following financial news article.
                
                Example 1
                Input1 (News Article):
                Emerging markets soared more than 33 percent in 2017, and Todd Gordon of TradingAnalysis.com says the rally won't stop. A big part of the rally in emerging markets, tracked by the emerging market ETF EEM , was a weak dollar. And given that Gordon still sees the inverse relationship between EEM and the dollar, measured in his charts by the dollar-tracking ETF UUP , he believes the U.S. currency will continue to help the group. "We have a falling U.S. dollar, which will support international and emerging market currencies and will give those EEM stocks a boost," Gordon said Tuesday on CNBC's "Trading Nation." The U.S. dollar in 2017 posted its worst annual performance in 14 years, while EEM saw its best performance since 2013. As for how high the latter could go, Gordon says EEM has broken "resistance" at around $45, which was the ETF's 2014 highs. That $45 region is now what he calls "support," and he sees it rallying to $50, which the ETF hasn't hit since mid-2011. To play for a move higher, Gordon suggested buying the February 48/50 call spread for 72 cents, or $72 per options contract. This means that if EEM closes above $50 on Feb. 16, then Gordon could make a maximum reward of $128 on the trade. But if EEM were to close below $48, then Gordon would lose the $72 he paid for the trade. As a result, Gordon wants to establish a point at which to get out. "If the 72 cent premium we just laid out gets cut in half to about 36 cents, let's cut the trade and move on," he said. EEM started the year off strong, rallying more than 1 percent on Tuesday.

                Input2 (Summary):
                The article discusses the strong performance of emerging markets in 2017, with a focus on the role of a weak U.S. dollar in driving the rally. Todd Gordon of TradingAnalysis.com suggests that the inverse relationship between the emerging market ETF (EEM) and the U.S. dollar (measured by the UUP ETF) will continue to benefit international and emerging market currencies. Gordon predicts a potential rise in EEM, citing a breakthrough in resistance at $45 and anticipates a rally to $50. He recommends an options trading strategy and sets conditions for exiting the trade. The article also mentions EEM's strong start in the current year, rallying over 1 percent on a specific day.

                Input3 (Economic Terms):
                Emerging Markets
                ETF (Exchange-Traded Fund)
                Rally
                Weak Dollar
                Inverse Relationship
                Currency
                Resistance and Support
                Options Contract
                Premium
                Maximum Reward
                Move Higher
                Call Spread
                Point of Exit
                Dollar-tracking ETF (UUP)
                Performance
                Annual Performance
                Point
                Resistance Broken
                February 48/50 Call Spread
                Cut the Trade

                Output:
                ###
                A group of countries with developing economies, characterized by rapid industrialization and higher-than-average growth rates.
                An investment fund that holds a diversified portfolio of assets like stocks or bonds and trades on the stock exchange.
                A sustained increase in the prices of financial instruments, such as stocks or bonds.
                A situation where the U.S. dollar has decreased in value compared to other currencies.
                A situation where the movement of one variable is opposite to the movement of another variable.
                A system of money used in a particular country or region.
                Technical analysis terms - Resistance is a price level at which a stock or market tends to stop rising, and support is a price level at which it tends to stop falling.
                A financial derivative that gives the holder the right, but not the obligation, to buy or sell an asset at a predetermined price before or at the expiration date.
                The amount paid for an options contract.
                The maximum profit that can be earned from a trade.
                Refers to an increase in the price or value of an asset.
                An options trading strategy involving both buying and selling call options on the same underlying asset with different strike prices or expiration dates.
                The predetermined level at which an investor decides to sell or exit a trade.
                An Exchange-Traded Fund that tracks the performance of the U.S. dollar against a basket of other currencies.
                The result or outcome of an investment over a specific period.
                The performance of an investment or market over the course of a year.
                Refers to a unit of measure in price movements.
                Indicates that the price has surpassed a previously challenging level.
                Refers to an options trading strategy involving buying a call option with a strike price of $48 and selling a call option with a strike price of $50.
                Deciding to exit or close a trade position.


                Input1 (News Article):
                {news_article}

                Input2 (Summary):
                {summary}

                Input3 (Economic Terms):
                {economic_terms_string}

                Output:
                ###
                """

    # Generate content using the prompt
    generated_content = model.generate_content(prompt).text

    # Split the generated content into definitions for each term
    definitions = [definition.strip()
                   for definition in generated_content.split('\n')]

    # Check if the number of generated definitions matches the number of economic terms
    if len(definitions) != len(economic_terms):
        raise ValueError(
            "The number of generated definitions does not match the number of economic terms.")
    return definitions


def start(news_article: str) -> Dict[str, List[str]]:
    """
    Starts the process of summarizing a financial news article, detecting economic terms, and getting definitions for the terms.

    Parameters:
    - news_article (str): The financial news article.

    Returns:
    - Dict[str, List[str]]: A dictionary containing the summary, economic terms, and definitions.
    """

    summary = summarize(news_article)
    terms = detect_economic_terms(news_article)
    definitions = get_economic_term_definitions(news_article, summary, terms)

    return summary, terms, definitions


news = input("news article: ")
summary, terms, definitions = start(news)

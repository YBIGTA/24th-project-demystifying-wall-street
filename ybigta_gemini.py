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
    Summarizes a economic news article using the GenerativeModel.

    Parameters:
    - news_article (str): The economic news article to be summarized.

    Returns:
    - str: The summary of the economic news article.
    """

    # Build a prompt for summarization
    prompt = f"""<<The following article is economic news article.
        Summarize the article.
        >>
        
        Input:
        {news_article}

        Output:
        ###
        """

    # Generate content
    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 250,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
        # stream=True,
    )
    if "**" in responses.text:
        return responses.text.replace("**", "")
    elif "*" in responses.text:
        return responses.text.replace("*", "")
    else:
        return responses.text


def detect_economic_terms(news_article: str) -> List[str]:
    """
    Tries to detect economic terms in a economic news article using the GenerativeModel.

    Parameters:
    - news_article (str): The economic news article to be analyzed.

    Returns:
    - List[str]: List of detected economic terms.
    """

    # Build a prompt for economic term detection
    prompt = f"""<<Identify economic jargon in the following economic news article.
                Provide only the jargon and avoid including definitions or explanations.
                
                Example1
                Input:
                Emerging markets soared more than 33 percent in 2017, and Todd Gordon of TradingAnalysis.com says the rally won't stop. A big part of the rally in emerging markets, tracked by the emerging market ETF EEM , was a weak dollar. And given that Gordon still sees the inverse relationship between EEM and the dollar, measured in his charts by the dollar-tracking ETF UUP , he believes the U.S. currency will continue to help the group. "We have a falling U.S. dollar, which will support international and emerging market currencies and will give those EEM stocks a boost," Gordon said Tuesday on CNBC's "Trading Nation." The U.S. dollar in 2017 posted its worst annual performance in 14 years, while EEM saw its best performance since 2013. As for how high the latter could go, Gordon says EEM has broken "resistance" at around $45, which was the ETF's 2014 highs. That $45 region is now what he calls "support," and he sees it rallying to $50, which the ETF hasn't hit since mid-2011. To play for a move higher, Gordon suggested buying the February 48/50 call spread for 72 cents, or $72 per options contract. This means that if EEM closes above $50 on Feb. 16, then Gordon could make a maximum reward of $128 on the trade. But if EEM were to close below $48, then Gordon would lose the $72 he paid for the trade. As a result, Gordon wants to establish a point at which to get out. "If the 72 cent premium we just laid out gets cut in half to about 36 cents, let's cut the trade and move on," he said. EEM started the year off strong, rallying more than 1 percent on Tuesday.

                Output:
                <<If there are the names of any celebrities, business professionals, company names, proper nouns, and common expressions, ignore them.>>
                ###
                1. Emerging Markets
                2. ETF (Exchange-Traded Fund)
                3. Rally
                4. Weak Dollar
                5. Inverse Relationship
                6. Currency
                7. Options Contract
                8. Premium
                9. Move Higher
                10. Call Spread
                11. Point of Exit
                12. Dollar-tracking ETF (UUP)
                13. Resistance Broken
                
                Example2
                Input:
                Published: Jan 2, 2018 5:59 p.m. ET Share Few mainstream investors have bought large sums of bitcoin, scared off by concerns about cybersecurity and liquidity Getty Images By Rob Copeland One of the biggest names in Silicon Valley is placing a moonshot bet on bitcoin BTCUSD, +0.72% . Founders Fund, the venture-capital firm co-founded by Peter Thiel, has amassed hundreds of millions of dollars of the volatile cryptocurrency, people familiar with the matter said. The bet has been spread across several of the firm's most recent funds, the people said, including one that began investing in mid-2017 and made bitcoin one of its first investments. Founders and Thiel, 50 years old, are well-known for early investments in companies like Facebook Inc. FB, +2.81% that sometimes take years to come to fruition. The bitcoin bet is quickly showing promise. Founders bought around $15 million to $20 million in bitcoin, and it has told investors the firm's haul is now worth hundreds of millions of dollars after the digital currency's ripping rise in the past year. It isn't clear if Founders has sold any of its holdings yet. The bet hasn't been previously reported.

                Output:
                <<If there are the names of any celebrities, business professionals, company names, proper nouns, and common expressions, ignore them.>>
                ###
                1. Moonshot bet
                2. Cryptocurrency
                3. Venture-capital firm
                4. Founders Fund
                5. Cybersecurity
                6. Liquidity
                7. Volatile
                8. Digital currency
                9. Ripping rise

                Example3
                Input:
                (Reuters) - Shares of Snap Inc sank as much as 22 percent to the lowest since its 2017 flotation on Wednesday, after first quarter numbers showed it losing confidence among users and advertisers due to a widely-panned redesign of Snapchat. The messaging app, known for its disappearing messages and ghost logo, started its first major redesign in November and followed up with several more updates this year. But the company is facing ire from users who say the changes are unnecessary and make the platform harder to use. A petition on change.org that urged the company to remove the update garnered more than 1.2 million signatures. The results release knocked another $4 billion off the value of the company, now down a total of $23 billion from its high point a day after its stock market launch last March. “It is not clear to us why the app redesign - the first product Snap ever tested at scale - was rolled out broadly, and we are even less clear on why it hasn't been more aggressively rolled back already,” Deutsche Bank analyst Lloyd Walmsley said. Company executives acknowledged that the new design hurt results but said they were sticking with the plan, aimed at broadening the app's popularity with users and advertisers. “The redesign created a lot of new opportunities, and we look forward to continuing our efforts to refine and improve Snapchat,” Snap's 27-year-old chief executive, Evan Spiegel, said on a conference call with analysts on Tuesday. Some analysts drew a stark comparison with Facebook Inc, which has also redesigned its platform without much backlash. Facebook, whose photo-sharing platform Instagram directly rivals Snapchat, last week reported a surprisingly strong 63 percent rise in profit and an increase in users, with no sign that business was hurt by a scandal over the mishandling of personal data. At least 13 brokerages cut their price targets on the stock. MoffettNathanson was the most bearish with a price target of $7. The stock is currently trading at $11.66. Snapchat's daily active users rose to 191 million in the quarter ended March 31, falling short of expectations of 194.15 million. Snap has also moved toward a software-based auction system for selling ads that made it cheaper and easier to buy ads on Snapchat, but hurts revenue on the short term. The company's revenue of $230.7 million also missed estimates of $244.5 million. While Snap can turn things around with its core base of users, Snap is a “show me” story to advertisers and investors, and has to move fast to change the narrative, particularly given its cash burn levels, Walmsley said. Snap said its cash burn fell 13 percent from the previous quarter to $222 million. Shares of Snap, which went public at a $17 tag, were last down 18.7 percent at $11.49. FILE PHOTO: The Snapchat messaging application is seen on a phone screen August 3, 2017. REUTERS/Thomas White/File Photo Reporting by Supantha Mukherjee and Munsif Vengattil in Bengaluru; editing by Anna Driver and Patrick Graham

                Output:
                <<If there are the names of any celebrities, business professionals, company names, proper nouns, and common expressions, ignore them.>>
                ###
                1. Shares
                2. Flotation
                3. First quarter numbers
                4. Redesign
                5. Petition on change.org
                6. Stock market launch
                7. Price targets
                8. Revenue
                9. Profit
                10. Brokerages
                11. Cash burn
                12. Tag

                Example4
                Input:
                For the past 10 years, the investment story on Apple was fairly straightforward. Investors and analysts only cared about how many iPhones it sold. And while that's still the primary metric for the company's success, it is no longer the only metric. The Apple story is more diversified than the company gets credit for, and Tuesday night's earnings report emphatically proves it. Apple sold 52.5 million iPhones in the first three months of 2018, missing analyst projections of 53 million units sold. That's a relatively meager 3 percent growth. As you can see in the chart below from Recode's Dan Frommer , Apple's unit growth has gone sideways for the past two years. And yet, Apple's shares since the start of 2016 are up a whopping 81 percent. The S&P 500 is only up 31 percent over the same period. Why is Apple on a tear? A few reasons. First and foremost: The iPhone, even at a low-to-no growth rate, is a killer business. It's highly profitable, and Apple has managed to raise the average price of the iPhone. show chapters Apple shares soar after announcing $100 billion buyback 3 Hours Ago | 01:50 With that cash machine, Apple has gone on a massive stock buyback run, while also raising its dividend. In the first three months of this year, Apple spent $23.5 billion on share repurchases. Since 2012, Apple has spent $200 billion on buying back its shares. It has returned an additional $75 billion to shareholders over that period in the form of dividends. And on Tuesday, it said it would initiate an additional $100 billion in stock repurchases. No matter what happens with the iPhone, in terms of growth, the fact that Apple has a $300 billion-plus stock buying bazooka helps to soften any blow in the growth of the iPhone for investors. But beyond that cash bazooka that is sitting on the desk of Apple's CFO, there's the fact that Apple has real growth in two new categories. On the call Tuesday night, Tim Cook said Apple's "wearables" business was up 50 percent and is now the size of a "Fortune 300" company. That implies its wearables — which include the Apple Watch, AirPods and Beats — is a $9 billion annual business, which is growing at a 50 percent rate. Cook said the Apple Watch grew at a "strong" double-digit rate and had its best ever March quarter performance. While many analysts and pundits like to focus on where Apple might be missing, they tend to overlook where it's hitting. And the wearable market between the watch and headphones appears to be dominated by Apple, with no real competition. The closest competitor is Fitbit, a $1.4 billion company whose sales and market value have tanked in the past year. Apple has the wearable market all to itself right now. And, all signs point toward Apple accelerating its development in the category. There are multiple reports that Apple is exploring the creation of a pair of augmented reality glasses. While Google , and others, have failed with glasses, Apple has a proven track record of selling sexy consumer computing products. Because of the failures by Google and others, there's a strong possibility that in five years, Apple will be owning the consumer's face with glasses, the consumer's wrist with the watch and the consumer's ears with AirPods. Meanwhile, the rest of the tech industry is fighting to sell people smart speakers for their kitchen. (Which, by the way, Apple is also doing, so it's not like it's totally whiffing on that category!) As they fight over that market, Apple is moving to own wearables. The final piece of the Apple story is services, which is Apple's App Store, Apple Music, iCloud and Apple Pay. Apple says it now has 270 million paid subscriptions, which is up 100 million on a year-over-year basis. Services delivered $9.2 billion in revenue, which was up 30 percent on a year-over-year basis. And, according to Cook, the services growth was global. He says the "minimum" growth for services was 25 percent in each geography. The services revenue is, for all intents and purposes, and ongoing tax on Apple's users. If you own an iPhone, you probably subscribe to iCloud to expand storage. If you own an iPhone, you probably download apps and make in-app purchases. If you own an iPhone, you might even be an Apple Music subscriber. Apple doesn't break out its margin on this business, but it would appear to be a relatively light lift for Apple, so it should be a highly profitable business since, and it should be a business that steady, and growing. So, in summary: Apple has a potentially great future business in wearables, it has an amazing current business with iPhones, and it has a nice steady recurring revenue business with services. No matter how negative analysts or pundits want to get around the iPhone, the simple fact of the matter is that Apple is well balanced for the future, just as much as any other major tech company.

                Output:
                <<If there are the names of any celebrities, business professionals, company names, proper nouns, and common expressions, ignore them.>>
                ###
                1. Stock Buyback
                2. Dividend
                3. Revenue
                4. Earnings Report
                5. Average Selling Price (ASP)
                6. Services Revenue
                7. Subscription
                8. Margin
                9. Recurring Revenue
                10. S&P 500
                11. Economic Diversification

                Example5
                Input:
                Top Wall Street analysts pick these 3 dividend stocks for the long haul A strong fourth-quarter earnings season is underway, and it’s time for dividend-paying companies to shine. Resilient dividend-paying companies can offer long-term growth potential and steady income. Investors ought to consider the insight of top Wall Street pros as they hunt for dividend stocks with solid fundamentals. Here are three attractive dividend stocks, according to Wall Street’s top experts on TipRanks, a platform that ranks analysts based on their past performance. Verizon Communications First up is telecom giant Verizon Communications (VZ), which recently reported its fourth-quarter results and impressed investors with the robust jump in wireless postpaid phone subscriber additions. In 2023, the company raised its dividend for the 17th consecutive year. Verizon’s quarterly dividend of $0.665 per share (annualized dividend of $2.66), reflects a yield of 6.7%. Following Verizon’s Q4 results, Tigress Financial analyst Ivan Feinseth reiterated a buy rating on the stock and increased the price target to $50 per share from $45. The analyst noted that the company delivered strong subscriber and cash flow growth in 2023, with further acceleration expected this year. “Ongoing 5G and fixed wireless broadband momentum and increased services offerings combined with operating efficiencies and margin improvement will drive a reacceleration in cash flow growth and improving Business Performance trends,” said Feinseth. The analyst thinks that Verizon’s solid balance sheet and cash flow support the company’s ongoing investments in spectrum expansion and other growth initiatives as well as dividend hikes. Overall, he thinks that the company offers a compelling investment opportunity, given its high dividend yield and industry-leading position that enables it to benefit from long-term telecom trends. Feinseth ranks No. 214 among more than 8,700 analysts tracked by TipRanks. His ratings have been profitable 61% of the time, with each delivering an average return of 11.7%. (See Verizon Hedge Fund Activity on TipRanks) Enterprise Products Partners This week’s second dividend pick is Enterprise Products Partners  (EPD), a master limited partnership that provides midstream energy services. Last month, the company announced a quarterly cash distribution of $0.515 per unit for the fourth quarter of 2023, to be paid on Feb. 14. This quarterly distribution marks a 5.1% year-over-year increase and reflects a yield of nearly 8%. In reaction to EPD’s fourth-quarter results, Stifel analyst Selman Akyol reaffirmed a buy rating on the stock and raised the price target to $36 per share from $35. The analyst stated that Q4 2023 results slightly surpassed his expectations. He increased his 2024 earnings before interest, tax, depreciation and amortization estimate by more than 2%, mainly due to the company’s natural gas liquids pipeline segment. Further, Akyol anticipates that the momentum in EPD’s pipeline and export throughputs will continue in the near term. The analyst also pointed out that EPD has increased its distributions for 25 years. He expects distributions to be the primary mode of returning capital to unitholders, with buybacks projected to be opportunistic. Explaining his investment stance, Akyol said, “We believe Enterprise has one of the strongest financial profiles within the midstream sector, and can withstand turbulence from a volatile macro environment.” Akyol holds the 695th position among more than 8,700 analysts tracked by TipRanks. His ratings have been profitable 64% of the time, with each delivering an average return of 5%. (See EPD Insider Trading Activity on TipRanks) MPLX LP Our third dividend pick is another midstream energy player, MPLX LP (MPLX). Last month, the master limited partnership announced a quarterly distribution of 85 cents per common unit for the fourth quarter of 2023, payable on Feb. 14. MPLX offers a dividend yield of 9%. Based on the recently announced fourth-quarter results, RBC Capital analyst Elvira Scotto reiterated a buy rating on MPLX stock and increased the price target to $46 per share from $45. The analyst noted that the company’s Q4 2023 adjusted EBITDA surpassed consensus expectations by 4%, thanks to increased product volumes, higher pipeline rates in the logistics and storage segment, and higher processing volumes in the gathering and processing unit. Given the high yield offered by the stock, Scotto thinks that MPLX remains one of the most attractive income plays in the large-cap MLP space. The analyst expects a cash distribution of $3.57 per unit in 2024 and $3.84 per unit in 2025. That’s up from $3.40 in 2023.  Scotto thinks that “future cash flow generation in conjunction with the financial flexibility provided by decreasing leverage and adequate distribution coverage can drive incremental capital returns to investors over time.”  Scotto ranks No. 83 among more than 8,700 analysts tracked by TipRanks. Her ratings have been profitable 64% of the time, with each delivering an average return of 17.8%. (See MPLX Technical Analysis on TipRanks)
                
                Output:
                <<If there are the names of any celebrities, business professionals, company names, proper nouns, and common expressions, ignore them.>>
                ###
                1. Dividend
                2. Haul
                3. Fourth-quarter earnings season
                4. Yield
                5. Q4 result
                6. Share
                7. Margin
                8. Cash flow growth
                9. Balance sheet
                10. Quarterly cash distribution
                11. Amortization estimate
                12. Capital
                13. Unitholder
                14. Buyback
                15. Payable
                16. RBC
                17. EBITDA
                18. Leverage
                19. Distribution coverage
                
                Input:
                {news_article}

                Output:
                <<If there are the names of any celebrities, business professionals, company names, proper nouns, and common expressions, ignore them.>>
                ###
                """

    # Generate content
    generated_content = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 100,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        })

    generated_content = generated_content.text

    # Extract economic terms
    economic_terms = [term.strip() for term in generated_content.split('\n')]

    # Remove empty strings
    economic_terms = [term for term in economic_terms if len(term) > 3]

    # Remove duplicates
    temp = [term.split(".", 1)[1] for term in economic_terms]
    temp = list(set(temp))
    economic_terms = [f'{i+1}.{term}' for i, term in enumerate(temp)]

    return economic_terms


def get_economic_term_definitions(news_article: str, economic_terms: List[str]) -> List[str]:
    """
    Gets definitions for given economic terms using a GenerativeModel.
    Definitions are generated based on the context of the input news article.

    Parameters:
    - news_article (str): The economic news article.
    - economic_terms (List[str]): List of economic terms.

    Returns:
    - List[str]: List of definitions for each economic term.
    """

    global model

    economic_terms_string = '\n'.join(economic_terms)

    # Build a prompt for definitions of multiple economic terms
    prompt = f"""<<Define the following economic jargon.
                Definitions should be based on the context of the following economic news article.
                The number of definitions should match the number of economic jargon.>>
                
                Example1
                Input1 (News Article):
                Emerging markets soared more than 33 percent in 2017, and Todd Gordon of TradingAnalysis.com says the rally won't stop. A big part of the rally in emerging markets, tracked by the emerging market ETF EEM , was a weak dollar. And given that Gordon still sees the inverse relationship between EEM and the dollar, measured in his charts by the dollar-tracking ETF UUP , he believes the U.S. currency will continue to help the group. "We have a falling U.S. dollar, which will support international and emerging market currencies and will give those EEM stocks a boost," Gordon said Tuesday on CNBC's "Trading Nation." The U.S. dollar in 2017 posted its worst annual performance in 14 years, while EEM saw its best performance since 2013. As for how high the latter could go, Gordon says EEM has broken "resistance" at around $45, which was the ETF's 2014 highs. That $45 region is now what he calls "support," and he sees it rallying to $50, which the ETF hasn't hit since mid-2011. To play for a move higher, Gordon suggested buying the February 48/50 call spread for 72 cents, or $72 per options contract. This means that if EEM closes above $50 on Feb. 16, then Gordon could make a maximum reward of $128 on the trade. But if EEM were to close below $48, then Gordon would lose the $72 he paid for the trade. As a result, Gordon wants to establish a point at which to get out. "If the 72 cent premium we just laid out gets cut in half to about 36 cents, let's cut the trade and move on," he said. EEM started the year off strong, rallying more than 1 percent on Tuesday.

                Input2 (Economic Jargon):
                1. Emerging Markets
                2. ETF (Exchange-Traded Fund)
                3. Rally
                4. Weak Dollar
                5. Inverse Relationship
                6. Currency
                7. Options Contract
                8. Premium
                9. Move Higher
                10. Call Spread
                11. Point of Exit
                12. Dollar-tracking ETF (UUP)
                13. Resistance Broken

                Output:
                <<Provide only the definitions and avoid highlighting or including the jargons themselves.>>
                ###
                1. A group of countries with developing economies, characterized by rapid industrialization and higher-than-average growth rates.
                2. An investment fund that holds a diversified portfolio of assets like stocks or bonds and trades on the stock exchange.
                3. A sustained increase in the prices of financial instruments, such as stocks or bonds.
                4. A situation where the U.S. dollar has decreased in value compared to other currencies.
                5. A situation where the movement of one variable is opposite to the movement of another variable.
                6. A system of money used in a particular country or region.
                7. A financial derivative that gives the holder the right, but not the obligation, to buy or sell an asset at a predetermined price before or at the expiration date.
                8. The amount paid for an options contract.
                9. Refers to an increase in the price or value of an asset.
                10. An options trading strategy involving both buying and selling call options on the same underlying asset with different strike prices or expiration dates.
                11. The predetermined level at which an investor decides to sell or exit a trade.
                12. An Exchange-Traded Fund that tracks the performance of the U.S. dollar against a basket of other currencies.
                13. Indicates that the price has surpassed a previously challenging level.

                Example2
                Input1 (News Article):
                Published: Jan 2, 2018 5:59 p.m. ET Share Few mainstream investors have bought large sums of bitcoin, scared off by concerns about cybersecurity and liquidity Getty Images By Rob Copeland One of the biggest names in Silicon Valley is placing a moonshot bet on bitcoin BTCUSD, +0.72% . Founders Fund, the venture-capital firm co-founded by Peter Thiel, has amassed hundreds of millions of dollars of the volatile cryptocurrency, people familiar with the matter said. The bet has been spread across several of the firm's most recent funds, the people said, including one that began investing in mid-2017 and made bitcoin one of its first investments. Founders and Thiel, 50 years old, are well-known for early investments in companies like Facebook Inc. FB, +2.81% that sometimes take years to come to fruition. The bitcoin bet is quickly showing promise. Founders bought around $15 million to $20 million in bitcoin, and it has told investors the firm's haul is now worth hundreds of millions of dollars after the digital currency's ripping rise in the past year. It isn't clear if Founders has sold any of its holdings yet. The bet hasn't been previously reported.

                Input2 (Economic Jargon):
                1. Moonshot bet
                2. Cryptocurrency
                3. Venture-capital firm
                4. Founders Fund
                5. Cybersecurity
                6. Liquidity
                7. Volatile
                8. Digital currency
                9. Ripping rise

                Output:
                <<Provide only the definitions and avoid highlighting or including the jargons themselves.>>
                ###
                1. A high-risk and ambitious investment with the potential for significant returns.
                2. A type of digital or virtual currency that uses cryptography for security and operates on a decentralized network.
                3. An investment firm that provides financial backing to startups and small businesses in exchange for ownership equity.
                4. An influential venture-capital firm co-founded by Peter Thiel that has made substantial investments in various companies.
                5. Measures and practices to protect computer systems, networks, and data from theft, damage, or unauthorized access.
                6. The ease with which an asset or security can be bought or sold in the market without affecting its price.
                7. Subject to rapid and unpredictable changes, often used to describe the price movements of financial instruments.
                8. A form of currency that exists only in electronic form and lacks a physical counterpart, such as Bitcoin.
                9. A significant and rapid increase in the value or price of a financial asset.

                Example3
                Input1 (News Article):
                (Reuters) - Shares of Snap Inc sank as much as 22 percent to the lowest since its 2017 flotation on Wednesday, after first quarter numbers showed it losing confidence among users and advertisers due to a widely-panned redesign of Snapchat. The messaging app, known for its disappearing messages and ghost logo, started its first major redesign in November and followed up with several more updates this year. But the company is facing ire from users who say the changes are unnecessary and make the platform harder to use. A petition on change.org that urged the company to remove the update garnered more than 1.2 million signatures. The results release knocked another $4 billion off the value of the company, now down a total of $23 billion from its high point a day after its stock market launch last March. “It is not clear to us why the app redesign - the first product Snap ever tested at scale - was rolled out broadly, and we are even less clear on why it hasn't been more aggressively rolled back already,” Deutsche Bank analyst Lloyd Walmsley said. Company executives acknowledged that the new design hurt results but said they were sticking with the plan, aimed at broadening the app's popularity with users and advertisers. “The redesign created a lot of new opportunities, and we look forward to continuing our efforts to refine and improve Snapchat,” Snap's 27-year-old chief executive, Evan Spiegel, said on a conference call with analysts on Tuesday. Some analysts drew a stark comparison with Facebook Inc, which has also redesigned its platform without much backlash. Facebook, whose photo-sharing platform Instagram directly rivals Snapchat, last week reported a surprisingly strong 63 percent rise in profit and an increase in users, with no sign that business was hurt by a scandal over the mishandling of personal data. At least 13 brokerages cut their price targets on the stock. MoffettNathanson was the most bearish with a price target of $7. The stock is currently trading at $11.66. Snapchat's daily active users rose to 191 million in the quarter ended March 31, falling short of expectations of 194.15 million. Snap has also moved toward a software-based auction system for selling ads that made it cheaper and easier to buy ads on Snapchat, but hurts revenue on the short term. The company's revenue of $230.7 million also missed estimates of $244.5 million. While Snap can turn things around with its core base of users, Snap is a “show me” story to advertisers and investors, and has to move fast to change the narrative, particularly given its cash burn levels, Walmsley said. Snap said its cash burn fell 13 percent from the previous quarter to $222 million. Shares of Snap, which went public at a $17 tag, were last down 18.7 percent at $11.49. FILE PHOTO: The Snapchat messaging application is seen on a phone screen August 3, 2017. REUTERS/Thomas White/File Photo Reporting by Supantha Mukherjee and Munsif Vengattil in Bengaluru; editing by Anna Driver and Patrick Graham

                Input2 (Economic Jargon):
                1. Shares
                2. Flotation
                3. First quarter numbers
                4. Redesign
                5. Petition on change.org
                6. Stock market launch
                7. Price targets
                8. Revenue
                9. Profit
                10. Brokerages
                11. Cash burn
                12. Tag

                Output:
                <<Provide only the definitions and avoid highlighting or including the jargons themselves.>>
                ###
                1. Refers to the ownership units in a company, often bought and sold on the stock market.
                2. The process by which a company goes public and its shares are made available for trading on a stock exchange.
                3. The financial results of a company for the first quarter of its fiscal year.
                4. The significant alteration of the appearance or functionality of a product, in this context, Snapchat.
                5. A formal request or appeal typically made by users on the change.org platform, often to gather support for a cause or request changes from a company.
                6. The initial public offering (IPO) when a company's shares are first made available for public trading.
                7. The projected future price of a stock as estimated by financial analysts.
                8. The total income generated by a company from its business operations.
                9. The financial gain made by a company when its revenue exceeds its expenses.
                10. Firms that facilitate the buying and selling of financial securities, acting as intermediaries between buyers and sellers.
                11. The rate at which a company is spending its cash reserves.
                12. The initial offering price of a company's shares when it goes public.

                Example4
                Input1 (News Article):
                For the past 10 years, the investment story on Apple was fairly straightforward. Investors and analysts only cared about how many iPhones it sold. And while that's still the primary metric for the company's success, it is no longer the only metric. The Apple story is more diversified than the company gets credit for, and Tuesday night's earnings report emphatically proves it. Apple sold 52.5 million iPhones in the first three months of 2018, missing analyst projections of 53 million units sold. That's a relatively meager 3 percent growth. As you can see in the chart below from Recode's Dan Frommer , Apple's unit growth has gone sideways for the past two years. And yet, Apple's shares since the start of 2016 are up a whopping 81 percent. The S&P 500 is only up 31 percent over the same period. Why is Apple on a tear? A few reasons. First and foremost: The iPhone, even at a low-to-no growth rate, is a killer business. It's highly profitable, and Apple has managed to raise the average price of the iPhone. show chapters Apple shares soar after announcing $100 billion buyback 3 Hours Ago | 01:50 With that cash machine, Apple has gone on a massive stock buyback run, while also raising its dividend. In the first three months of this year, Apple spent $23.5 billion on share repurchases. Since 2012, Apple has spent $200 billion on buying back its shares. It has returned an additional $75 billion to shareholders over that period in the form of dividends. And on Tuesday, it said it would initiate an additional $100 billion in stock repurchases. No matter what happens with the iPhone, in terms of growth, the fact that Apple has a $300 billion-plus stock buying bazooka helps to soften any blow in the growth of the iPhone for investors. But beyond that cash bazooka that is sitting on the desk of Apple's CFO, there's the fact that Apple has real growth in two new categories. On the call Tuesday night, Tim Cook said Apple's "wearables" business was up 50 percent and is now the size of a "Fortune 300" company. That implies its wearables — which include the Apple Watch, AirPods and Beats — is a $9 billion annual business, which is growing at a 50 percent rate. Cook said the Apple

                Input2 (Economic Jargon):
                1. Stock Buyback
                2. Dividend
                3. Revenue
                4. Earnings Report
                5. Average Selling Price (ASP)
                6. Services Revenue
                7. Subscription
                8. Margin
                9. Recurring Revenue
                10. S&P 500
                11. Economic Diversification

                Output:
                <<Provide only the definitions and avoid highlighting or including the jargons themselves.>>
                ###
                1. A corporate action where a company repurchases its own shares from the open market, reducing the number of outstanding shares.
                2. A payment made by a corporation to its shareholders, usually in the form of cash or additional shares, as a share of the company's profits.
                3. The total income generated by a company from its primary operations, often expressed in monetary terms.
                4. A financial statement released by a company that summarizes its financial performance over a specific period, typically a quarter or a year.
                5. The average price at which a company sells its products, calculated by dividing the total revenue by the number of units sold.
                6. Income generated by a company through the provision of services rather than the sale of physical goods.
                7. A recurring payment made by a customer for continued access to a product or service, such as subscription-based streaming or software services.
                8. The difference between the cost of producing a product or service and its selling price, often expressed as a percentage.
                9. Revenue that a company can reliably anticipate earning on a regular basis, typically through subscription or ongoing service fees.
                10. A stock market index that measures the performance of 500 large companies listed on stock exchanges in the United States.
                11. The strategy of expanding a business or economy by investing in different sectors or products to reduce risk and reliance on a single source of revenue.

                Example5
                Input1 (News Article):
                Top Wall Street analysts pick these 3 dividend stocks for the long haul A strong fourth-quarter earnings season is underway, and it’s time for dividend-paying companies to shine. Resilient dividend-paying companies can offer long-term growth potential and steady income. Investors ought to consider the insight of top Wall Street pros as they hunt for dividend stocks with solid fundamentals. Here are three attractive dividend stocks, according to Wall Street’s top experts on TipRanks, a platform that ranks analysts based on their past performance. Verizon Communications First up is telecom giant Verizon Communications (VZ), which recently reported its fourth-quarter results and impressed investors with the robust jump in wireless postpaid phone subscriber additions. In 2023, the company raised its dividend for the 17th consecutive year. Verizon’s quarterly dividend of $0.665 per share (annualized dividend of $2.66), reflects a yield of 6.7%. Following Verizon’s Q4 results, Tigress Financial analyst Ivan Feinseth reiterated a buy rating on the stock and increased the price target to $50 per share from $45. The analyst noted that the company delivered strong subscriber and cash flow growth in 2023, with further acceleration expected this year. “Ongoing 5G and fixed wireless broadband momentum and increased services offerings combined with operating efficiencies and margin improvement will drive a reacceleration in cash flow growth and improving Business Performance trends,” said Feinseth. The analyst thinks that Verizon’s solid balance sheet and cash flow support the company’s ongoing investments in spectrum expansion and other growth initiatives as well as dividend hikes. Overall, he thinks that the company offers a compelling investment opportunity, given its high dividend yield and industry-leading position that enables it to benefit from long-term telecom trends. Feinseth ranks No. 214 among more than 8,700 analysts tracked by TipRanks. His ratings have been profitable 61% of the time, with each delivering an average return of 11.7%. (See Verizon Hedge Fund Activity on TipRanks) Enterprise Products Partners This week’s second dividend pick is Enterprise Products Partners  (EPD), a master limited partnership that provides midstream energy services. Last month, the company announced a quarterly cash distribution of $0.515 per unit for the fourth quarter of 2023, to be paid on Feb. 14. This quarterly distribution marks a 5.1% year-over-year increase and reflects a yield of nearly 8

                Input2 (Economic Jargon):
                1. Dividend
                2. Haul
                3. Fourth-quarter earnings season
                4. Yield
                5. Q4 result
                6. Share
                7. Margin
                8. Cash flow growth
                9. Balance sheet
                10. Quarterly cash distribution
                11. Amortization estimate
                12. Capital
                13. Unitholder
                14. Buyback
                15. Payable
                16. RBC
                17. EBITDA
                18. Leverage
                19. Distribution coverage

                Output:
                <<Provide only the definitions and avoid highlighting or including the jargons themselves.>>
                ###
                1. A payment made by a corporation to its shareholders, usually in the form of cash or additional shares.
                2. The act of transporting goods for an extended period, typically referring to a long-term investment perspective in the stock market.
                3. The period encompassing the final three months of the fiscal year when companies report their financial results.
                4. The income generated by an investment, typically expressed as a percentage of the investment's cost.
                5. The financial outcomes and figures reported by a company for the fourth quarter of its fiscal year.
                6. A unit of ownership in a company, representing a proportionate claim on its assets and earnings.
                7. The difference between revenue and the cost of goods sold, often expressed as a percentage.
                8. The percentage increase in a company's net cash flow over a specific period, indicating financial health.
                9. A financial statement showing a company's assets, liabilities, and shareholders' equity at a specific point in time.
                10. The periodic payment made by a company to its shareholders, typically in the form of cash or additional shares.
                11. An estimate of the gradual reduction in the value of an intangible asset over time.
                12. Financial resources available for use in the production of goods or services, often in the form of money or assets.
                13. An individual or entity that holds units or shares in a partnership or corporation.
                14. The repurchase of a company's own shares, reducing the number of outstanding shares.
                15. The date on which a payment, such as dividends, is scheduled to be made.
                16. Royal Bank of Canada, a multinational financial services company.
                17. Earnings Before Interest, Taxes, Depreciation, and Amortization, a measure of a company's operating performance.
                18. The use of borrowed capital to increase the potential return of an investment.
                19. The extent to which a company's earnings can cover its dividend payments, indicating financial sustainability.

                Input1 (News Article):
                {news_article}

                Input2 (Economic Jargon):
                {economic_terms_string}

                Output:
                <<Provide only the definitions and avoid highlighting or including the jargons themselves.>>
                ###
                """

    # Generate content using the prompt
    generated_content = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        })

    generated_content = generated_content.text

    # Split the generated content into definitions for each term
    definitions = [definition.strip()
                   for definition in generated_content.split('\n')]

    # If the number of definitions is not equal to the number of economic terms, try again
    if len(definitions) != len(economic_terms):
        model = GenerativeModel("gemini-pro")
        definitions = get_economic_term_definitions(
            news_article, summary, economic_terms)
    return definitions


def start(news_article: str) -> Dict[str, List[str]]:
    """
    Starts the process of summarizing a economic news article, detecting economic terms, and getting definitions for the terms.

    Parameters:
    - news_article (str): The economic news article.

    Returns:
    - Dict[str, List[str]]: A dictionary containing the summary, economic terms, and definitions.
    """

    summary = summarize(news_article)
    terms = detect_economic_terms(news_article)
    definitions = get_economic_term_definitions(news_article, terms)

    return summary, terms, definitions


news = input("news article: ")
summary, terms, definitions = start(news)
print()
print("summary: ", summary)
print()
print("terms: ", terms)
print()
print("definitions: ", definitions)

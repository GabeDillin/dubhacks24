## Inspiration
In a fast-paced world filled with daily stress and limited time for self-care, we recognized the need for personalized travel solutions. Vacations and trips are fantastic ways to rejuvenate, but planning them can often be overwhelming, time-consuming, and difficult to tailor to personal preferences. We wanted to create a tool that simplifies this process, making it easy for anyone to plan the perfect wellness getaway, whether it’s for relaxation, adventure, or mental clarity. This inspired us to build TravelAI, combining our passion for vacation with the power of AI.

## What it does
TravelAI is a smart app that creates personalized itineraries for vacations. Users simply input their preferences, such as preferred destination, the activities they are interested in, and how long they plan to stay. The app uses AI to curate a perfect itinerary tailored to the user’s needs, including accommodations, activities, local wellness spots, and even meal suggestions that promote well-being. It takes the stress out of planning, allowing users to focus on enjoying their rejuvenation journey.

## How we built it
Implemented perplexity LLM along with Amadeus flights API secured using OAuth and verification. Used Figma and React to design and develop the front end. Provisioned a SQL database and Azure connection with Terraform for future development. Also secured environment variables and API keys with a Terraform CICD pipeline on Github actions.

## Challenges we ran into
Additionally, integrating multiple APIs to pull travel data, wellness services, and local information in real-time required fine-tuning to ensure accuracy and user satisfaction. Another challenge was designing an interface that was both intuitive and flexible, so users with various levels of tech-savviness could easily navigate the app.

The hardest challenge was getting the Perplexity API to output a valid JSON object that we could parse for the frontend. We ran into issues with the variability of outputs, and we had to experiment with prompts and temperature of the model.

## Accomplishments that we're proud of
Getting a MVP by the end time. Working together with four team members that we've never worked with before.

## What we learned
Lots of new experiences with new frameworks and tools. 

## What's next for TravelAI
Aside from finishing refining the UI, we envision TravelAI evolving into a comprehensive travel platform, not just limited to trip planning but also providing ongoing wellness support, such as daily mindfulness tips, meditation guides, and local community recommendations. We plan to expand our partnerships with more wellness service providers and enhance the app’s AI to offer even more personalized and flexible options. Additionally, we aim to introduce a social component where users can share their trip experiences, tips, and recommendations with the community. In the future, we hope to integrate sustainable travel options, encouraging eco-friendly wellness journeys.

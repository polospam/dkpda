import hashlib
from sqlalchemy import select
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from bkend import models
from bkend.schemas import ArticleCreate, Category
from bkend.crud import create_user, get_user_by_email, create_article, get_articles_with_votes



PWD_CONTEXT = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


SEED_ARTICLES = [
    ArticleCreate(
        title="Government Shutdown Enters Third Week; No One Notices",
        content=(
            "WASHINGTON, D.C. — The federal government officially entered its third week of "
            "a complete shutdown on Monday, and according to multiple sources, absolutely no "
            "one has noticed.\n\n"
            "\"I just assumed everything was running normally,\" said Karen Bellweather, a "
            "retired schoolteacher from Ohio. \"The potholes are the same size, the DMV still "
            "takes four hours, and my congressman still hasn't returned my email from 2019. "
            "What exactly changed?\"\n\n"
            "Government analysts confirmed that all measurable metrics of federal performance "
            "— including response times, public satisfaction, and overall effectiveness — "
            "have remained statistically identical to pre-shutdown levels.\n\n"
            "\"We ran the numbers three times,\" said Dr. Helen Park, a public policy "
            "researcher at Georgetown. \"There is literally no difference. If anything, the "
            "national parks are slightly cleaner because nobody's there to leave the porta-"
            "potties unlocked.\"\n\n"
            "Congress has scheduled an emergency session to address the crisis but reportedly "
            "cannot agree on which day of the week it is."
        ),
        image_url="./media/gvmtshtdwn.webp",
        category=Category.GRAFT,
    ),
    ArticleCreate(
        title="Crypto Moguls Announce Plans to Buy Their Own Country, Immediately Disagree on Constitution",
        content=(
            "MIAMI — A consortium of cryptocurrency billionaires announced Tuesday their "
            "ambitious plan to purchase a small Pacific island nation and establish a "
            "blockchain-based libertarian paradise. The project collapsed within 72 hours "
            "when founders could not agree on a governance framework.\n\n"
            "\"We all agreed that the old system is broken,\" explained co-founder Chad "
            "Ledger, speaking from the deck of his rented yacht. \"Where we disagree is "
            "on literally everything else. Kyle wants proof-of-stake voting. Braden insists "
            "on a DAO-based judiciary. And someone named @CryptoViking69 keeps proposing "
            "trial by combat.\"\n\n"
            "The island's existing residents, a fishing community of about 300 people, "
            "expressed relief at the project's failure. \"They offered us forty million "
            "dollars in a currency that lost half its value during the sales pitch,\" said "
            "village elder Tui Manu. \"We politely declined.\"\n\n"
            "At press time, the consortium had pivoted to building a floating city, "
            "which experts say will sink both literally and financially within the first "
            "fiscal quarter."
        ),
        image_url="./media/crypto-moguls.webp",
        category=Category.GRIFT,
    ),
    ArticleCreate(
        title="Argentine President Declares Free Markets Are Great Except for the Parts That Apply to Argentina",
        content=(
            "BUENOS AIRES — Argentine President Javier Milei held an impassioned press "
            "conference Thursday in which he praised the invisible hand of the free market "
            "while simultaneously announcing a new round of exchange rate controls, export "
            "restrictions, and what he described as \"freedom-compatible subsidies.\"\n\n"
            "\"Let me be absolutely clear,\" Milei said, slamming a copy of \"The Road to "
            "Serfdom\" on the podium. \"Free markets are the only path to prosperity. "
            "However, Argentina's markets require a brief period of government intervention "
            "in order to become free. It's like a caterpillar. You have to trap it in a jar "
            "before it can become a butterfly.\"\n\n"
            "Economists were divided on the analogy. \"That's not how butterflies work,\" "
            "said Dr. Sofia Herrera of the University of Buenos Aires. \"And it's definitely "
            "not how markets work either.\"\n\n"
            "The IMF, which recently approved a $20 billion support package for Argentina, "
            "released a two-word statement in response: \"We know.\""
        ),
        image_url="./media/milei.jpeg",
        category=Category.CRONY,
    ),
    ArticleCreate(
        title="World Leaders Describe Peace Deal as 'Historic' Despite Neither Side Reading It",
        content=(
            "GENEVA — In what diplomats are calling a breakthrough for international "
            "relations, two nations locked in a decades-long territorial dispute signed "
            "a comprehensive peace agreement Wednesday that neither side's leadership "
            "has actually read.\n\n"
            "\"This is a momentous occasion,\" declared the lead negotiator, gesturing "
            "broadly at a 400-page document on the table. \"Both parties have agreed to "
            "the terms, which I'm told are in there somewhere. The important thing is the "
            "photo op.\"\n\n"
            "Sources close to the negotiations revealed that the final draft was produced "
            "at 3 a.m. by a team of exhausted junior diplomats who \"mostly copied and "
            "pasted from a 1997 trade agreement and hoped no one would check.\"\n\n"
            "\"We're thrilled with the outcome,\" said a spokesperson for one of the "
            "signatory nations. When asked which specific provisions they found most "
            "favorable, the spokesperson smiled, said \"all of them,\" and quickly left "
            "the room.\n\n"
            "International law experts predict the agreement will hold for approximately "
            "as long as it takes someone to read page 214, which accidentally cedes "
            "a major seaport to a country that was not part of the negotiations."
        ),
        image_url="./media/trump-zelensky.webp",
        category=Category.NONSENSE,
    ),
    ArticleCreate(
        title="AI Chatbot Hired as Congressional Aide Outperforms Entire Staff by Doing Absolutely Nothing",
        content=(
            "WASHINGTON, D.C. — An artificial intelligence chatbot quietly installed as "
            "a legislative aide in a congressman's office has reportedly outperformed "
            "the entire human staff by virtue of doing absolutely nothing.\n\n"
            "\"It hasn't introduced a single piece of harmful legislation, it hasn't "
            "leaked anything to the press, and it hasn't been caught in a lobbying "
            "scandal,\" said Chief of Staff Donna Whitfield. \"Honestly, it's our best "
            "hire in twenty years.\"\n\n"
            "The chatbot, a standard large language model given the title \"Senior Policy "
            "Advisor,\" reportedly spends its days generating polite non-answers to "
            "constituent emails — a task previously requiring a team of six.\n\n"
            "\"Dear concerned citizen, thank you for your heartfelt letter about "
            "infrastructure,\" read one such response. \"Rest assured, we take this matter "
            "very seriously and will continue to monitor the situation. Best regards.\"\n\n"
            "When asked if the chatbot would eventually replace the congressman himself, "
            "Whitfield paused and said, \"Let's not get ahead of ourselves. But also, "
            "we're not ruling it out.\""
        ),
        image_url="./media/inauguration.webp",
        category=Category.AI,
    ),
    ArticleCreate(
        title="Billionaire Philanthropist Donates $50 Million to Name a Building After Himself That Helps No One",
        content=(
            "NEW YORK — Tech billionaire Preston Hale III announced a landmark $50 million "
            "donation this week to construct the Preston Hale III Center for Transformative "
            "Synergies, a gleaming 12-story building in midtown Manhattan that will help "
            "absolutely no one.\n\n"
            "\"This is about giving back,\" Hale said at a press conference held inside "
            "a different building he had previously named after himself. \"When I look at "
            "the challenges facing humanity — poverty, disease, climate change — I think, "
            "'What if there were a really impressive lobby with my name on it?'\"\n\n"
            "The Center for Transformative Synergies will feature a rooftop meditation "
            "garden accessible only to donors, a thought-leadership incubation lounge, "
            "and a 40-foot bronze statue of Hale in what architects describe as a "
            "\"contemplative power pose.\"\n\n"
            "Tax experts noted that the donation will save Hale approximately $47 million "
            "in taxes, making the effective cost of his generosity roughly equivalent to "
            "a mid-range sedan.\n\n"
            "\"It's the thought that counts,\" said Hale's publicist, \"and Preston has "
            "thought about this building a lot.\""
        ),
        image_url="./media/planetower.webp",
        category=Category.GRIFT,
    ),
    ArticleCreate(
        title="Study Finds 97% of 'Reply All' Emails Could Have Been Replaced by Silence",
        content=(
            "CAMBRIDGE, MA — Researchers at MIT released a groundbreaking study Monday "
            "finding that 97 percent of all \"Reply All\" emails sent in corporate "
            "environments could have been replaced by simply doing nothing.\n\n"
            "\"We analyzed 14 million workplace emails across 200 companies,\" said lead "
            "researcher Dr. Anil Gupta. \"The overwhelming majority of Reply All messages "
            "consisted of 'Thanks!', 'Sounds good!', 'Looping in Jeff,' and one person "
            "who accidentally shared their grocery list with the entire legal department.\"\n\n"
            "The study estimated that eliminating unnecessary Reply All emails would save "
            "the American economy approximately $4.6 billion annually in lost productivity, "
            "plus an incalculable amount of emotional damage.\n\n"
            "Corporate executives responded to the findings with cautious optimism. "
            "\"We're committed to reducing Reply All abuse,\" wrote one Fortune 500 CEO "
            "in a company-wide email sent to 40,000 employees. Fourteen thousand of them "
            "replied all to say they agreed.\n\n"
            "Dr. Gupta's team is reportedly now studying an even more destructive "
            "workplace phenomenon: the meeting that could have been an email that could "
            "have been nothing."
        ),
        image_url="./media/inauguration.webp",
        category=Category.NONSENSE,
    ),
    ArticleCreate(
        title="Nation's Leaders Assure Public That Unprecedented Crisis Is Actually a Tremendous Opportunity",
        content=(
            "WASHINGTON, D.C. — As the nation grapples with what experts are calling an "
            "\"unprecedented, multi-layered catastrophe,\" leaders from both parties held "
            "a rare joint press conference Monday to assure the public that the crisis is, "
            "in fact, a tremendous opportunity.\n\n"
            "\"Every generation faces a defining challenge,\" said the Senate Majority "
            "Leader, reading from a prepared statement. \"For our grandparents it was the "
            "Great Depression. For our parents, the Cold War. For us, it's this thing that "
            "I'm told is very bad but that I'm choosing to frame as exciting.\"\n\n"
            "The House Speaker echoed the sentiment. \"In times like these, Americans don't "
            "ask 'Why us?' They ask 'How can we leverage this into a midterm campaign "
            "slogan?' And I think that's beautiful.\"\n\n"
            "A bipartisan task force has been assembled to study the crisis, with its first "
            "report expected in eighteen months — roughly six months after the crisis is "
            "projected to resolve itself without any government involvement whatsoever.\n\n"
            "At press time, both parties had released competing fundraising emails about "
            "the opportunity, each blaming the other for it."
        ),
        image_url="./media/trump-putin.jpeg",
        category=Category.GRAFT,
    ),
]


def get_password_hash(password: str) -> str:
    """Match the application's pre-hash + CryptContext logic.

    We compute SHA-256 hex digest then hash that with the configured
    CryptContext so produced hashes match those generated by the app.
    """
    if isinstance(password, str):
        pw_bytes = password.encode("utf-8")
    else:
        pw_bytes = password
    sha_hex = hashlib.sha256(pw_bytes).hexdigest()
    return PWD_CONTEXT.hash(sha_hex)


def main() -> None:
    """Populate the database with an admin user, if one does not already exist,
    or promote the existing user to admin..

    Run from the project root:  python -m bkend.scripts.populate_db
    """
    models.init_db()
    email = "admin@ex.com"
    raw_password = "pass"

    with Session(models.engine) as db:
        user = get_user_by_email(db, email=email)
        if user:
            if getattr(user, "is_admin", False):
                print(f"User {email} already exists and is an admin")
                articles = get_articles_with_votes(db, user.id)
                print("Articles in db: ", articles)
                return
            user.is_admin = True
            db.commit()
            print(f"Existing user {email} promoted to admin")
            return

        hashed = get_password_hash(raw_password)
        create_user(db, email=email, hashed_password=hashed)
        # Ensure the created user is marked admin
        created = get_user_by_email(db, email=email)
        if created:
            created.is_admin = True
            db.commit()
            print(f"Created admin user {email} with password '{raw_password}'")
        else:
            print("Failed to create admin user")

        # Create satirical articles authored by the admin if they don't exist
        admin_user = created
        if admin_user:
            existing_articles = db.execute(select(models.Article)).scalars().all()
            if not existing_articles:
                print("Adding satirical articles...")
                for art_data in SEED_ARTICLES:
                    create_article(db, art_data, author_id=admin_user.id)
                print(f"Added {len(SEED_ARTICLES)} satirical articles")
            else:
                print("Articles already present; skipping article creation")


# Helper function to update the image_url of an article by its id
def update_article_image_url(db: Session, article_id: int, new_image_url: str) -> None:
    article = db.get(models.Article, article_id)
    if article:
        article.image_url = new_image_url
        db.commit()


# Function to update image URLs of existing articles; takes a list of tuples (id, new_url)
def update_existing_articles_images(articles: list[tuple[int, str]]) -> None:
    models.init_db()
    with Session(models.engine) as db:
        for article_id, new_url in articles:
            update_article_image_url(db, article_id, new_url)
            print(f"Updated article id {article_id} image_url to {new_url}")


if __name__ == "__main__":
    main()

    articles_to_update = [
        (1, "./media/planetower.webp"),
        (2, "./media/crypto-moguls.webp"),
        (3, "./media/milei.jpeg"),
        (4, "./media/trump-zelensky.webp"),
    ]
    update_existing_articles_images(articles_to_update)
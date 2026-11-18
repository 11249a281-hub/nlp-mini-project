import streamlit as st
import re
from collections import Counter
from datetime import datetime

st.set_page_config(
    page_title="Canteen Review Analyzer",
    page_icon="🍽️",
    layout="wide"
)

# Sentiment words
positive_words = [
    "good", "tasty", "fresh", "excellent", "delicious",
    "clean", "affordable", "friendly", "nice", "best",
    "great", "happy", "quality", "fast", "reasonable"
]

negative_words = [
    "bad", "dirty", "slow", "stale", "expensive",
    "poor", "worst", "crowded", "unhygienic",
    "cold", "rude", "costly", "waste"
]

# Aspect keywords
aspects = {
    "Food Quality": [
        "food", "taste", "tasty", "fresh", "stale",
        "meal", "meals", "delicious"
    ],
    "Cleanliness": [
        "clean", "dirty", "hygiene", "tables"
    ],
    "Price": [
        "price", "affordable", "expensive", "cost",
        "cheap", "costly"
    ],
    "Service": [
        "service", "staff", "friendly", "slow",
        "queue", "waiting"
    ],
    "Ambience": [
        "seating", "seat", "crowded", "place",
        "space", "ambience"
    ]
}

# Project title
st.title("🍽️ College Canteen Review Analyzer")
st.subheader("An NLP-Based System")
st.write("Analyze student feedback automatically using NLP.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Dashboard", "Review Analysis", "About Project"]
)

# Sample reviews
sample_reviews = """The food is tasty and fresh.
The canteen tables are dirty.
The price is affordable.
The service is very slow.
The staff are friendly.
The seating area is crowded."""

# NLP analysis function
def analyze_review(review):

    words = re.findall(r"[a-zA-Z]+", review.lower())

    pos_count = sum(
        1 for word in words if word in positive_words
    )

    neg_count = sum(
        1 for word in words if word in negative_words
    )

    if pos_count > neg_count:
        sentiment = "Positive"

    elif neg_count > pos_count:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    found_aspects = []

    for aspect, keywords in aspects.items():

        if any(word in words for word in keywords):
            found_aspects.append(aspect)

    return words, sentiment, found_aspects


# Session storage
if "results" not in st.session_state:
    st.session_state.results = []

if "reviews" not in st.session_state:
    st.session_state.reviews = []


# Dashboard
if page == "Dashboard":

    st.header("📊 Dashboard Overview")

    results = st.session_state.results

    total = len(results)

    positive = sum(
        1 for r in results if r["sentiment"] == "Positive"
    )

    negative = sum(
        1 for r in results if r["sentiment"] == "Negative"
    )

    neutral = sum(
        1 for r in results if r["sentiment"] == "Neutral"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Reviews", total)
    c2.metric("Positive", positive)
    c3.metric("Negative", negative)
    c4.metric("Neutral", neutral)

    st.subheader("Sentiment Distribution")

    if total > 0:

        st.bar_chart({
            "Reviews": {
                "Positive": positive,
                "Negative": negative,
                "Neutral": neutral
            }
        })

    else:
        st.info("Analyze some reviews to view dashboard results.")


# Review Analysis
elif page == "Review Analysis":

    st.header("📝 Student Review Analysis")

    uploaded_file = st.file_uploader(
        "Upload Review Text File",
        type=["txt"]
    )

    review_input = sample_reviews

    if uploaded_file is not None:
        review_input = uploaded_file.read().decode("utf-8")

    review_input = st.text_area(
        "Enter student reviews (one review per line)",
        value=review_input,
        height=180
    )

    if st.button("🔍 Analyze Reviews"):

        reviews = [
            line.strip()
            for line in review_input.splitlines()
            if line.strip()
        ]

        results = []

        for review in reviews:

            words, sentiment, found_aspects = analyze_review(review)

            results.append({
                "review": review,
                "tokens": words,
                "sentiment": sentiment,
                "aspects": found_aspects
            })

        st.session_state.results = results
        st.session_state.reviews = reviews

    results = st.session_state.results

    if results:

        st.divider()

        st.subheader("Review-wise Results")

        for i, result in enumerate(results, 1):

            with st.expander(f"Review {i}"):

                st.write("Review:", result["review"])

                st.write("Sentiment:", result["sentiment"])

                st.write(
                    "Aspects:",
                    ", ".join(result["aspects"])
                    if result["aspects"] else "Not identified"
                )

                st.write(
                    "Tokens:",
                    ", ".join(result["tokens"])
                )

        # Sentiment counts
        positive = sum(
            1 for r in results if r["sentiment"] == "Positive"
        )

        negative = sum(
            1 for r in results if r["sentiment"] == "Negative"
        )

        neutral = sum(
            1 for r in results if r["sentiment"] == "Neutral"
        )

        st.subheader("📈 Sentiment Analysis")

        st.bar_chart({
            "Reviews": {
                "Positive": positive,
                "Negative": negative,
                "Neutral": neutral
            }
        })

        # Aspect analysis
        st.subheader("Aspect Identification")

        aspect_count = Counter()

        for result in results:
            aspect_count.update(result["aspects"])

        if aspect_count:
            st.bar_chart(dict(aspect_count))

        # Keyword extraction
        st.subheader("Important Keywords")

        stop_words = [
            "the", "is", "and", "are", "was", "a",
            "an", "of", "to", "in", "very", "but"
        ]

        all_words = []

        for result in results:
            all_words.extend(result["tokens"])

        keywords = Counter(
            word for word in all_words
            if len(word) > 2 and word not in stop_words
        )

        for word, count in keywords.most_common(10):
            st.write(word, ":", count)

        # Summary
        st.subheader("Overall Summary")

        st.success(
            f"Total {len(results)} reviews: "
            f"{positive} Positive, "
            f"{negative} Negative, "
            f"{neutral} Neutral."
        )

        # Generate report
        report = "COLLEGE CANTEEN REVIEW ANALYZER\n"
        report += "=" * 40 + "\n"
        report += "Date: " + datetime.now().strftime("%d-%m-%Y") + "\n\n"

        for i, result in enumerate(results, 1):

            report += f"Review {i}: {result['review']}\n"
            report += f"Sentiment: {result['sentiment']}\n"
            report += f"Aspects: {', '.join(result['aspects'])}\n\n"

        report += "\nOVERALL SUMMARY\n"
        report += f"Positive: {positive}\n"
        report += f"Negative: {negative}\n"
        report += f"Neutral: {neutral}\n"

        report += "\nIMPORTANT KEYWORDS\n"

        for word, count in keywords.most_common(10):
            report += f"{word}: {count}\n"

        st.download_button(
            "⬇️ Download Analysis Report",
            data=report,
            file_name="canteen_review_report.txt",
            mime="text/plain"
        )


# About Project
elif page == "About Project":

    st.header("📚 About Our Project")

    st.write("""
    College Canteen Review Analyzer is an NLP-based
    application used to analyze student feedback.

    It identifies positive, negative and neutral reviews.

    It also detects food quality, cleanliness, price,
    service and ambience.
    """)

    st.subheader("Technologies Used")

    st.write("""
    - Python
    - Natural Language Processing
    - Regular Expressions
    - Collections Counter
    - Streamlit
    """)

    st.subheader("Project Team")

    st.write("1. P. Lahari - 11249A281")
    st.write("2. M. Vaidhya Nadeswar Reddy - 11249A239")
    st.write("3. M. Harshavardhan Krishna - 11249A210")

    st.success("Academic Year: 2026-2027")

st.divider()

st.caption("College Canteen Review Analyzer | NLP Mini Project")

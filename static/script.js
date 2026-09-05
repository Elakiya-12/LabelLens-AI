// ============================================================
// LABEL LENS AI - FINAL JAVASCRIPT
// ============================================================


// ============================================================
// GET HTML ELEMENTS
// ============================================================

const imageUpload = document.getElementById("imageUpload");

const previewSection =
    document.getElementById("previewSection");

const previewImage =
    document.getElementById("previewImage");

const analyzeButton =
    document.getElementById("analyzeButton");

const resultSection =
    document.getElementById("resultSection");

const ingredientList =
    document.getElementById("ingredientList");

const skinSection =
    document.getElementById("skinSection");

const skinType =
    document.getElementById("skinType");

const analysisSection =
    document.getElementById("analysisSection");

const analysisResults =
    document.getElementById("analysisResults");

const ingredientInput =
    document.getElementById("ingredientInput");

const textAnalyzeButton =
    document.getElementById("textAnalyzeButton");


// ============================================================
// STORE EXTRACTED INGREDIENTS
// ============================================================

let extractedIngredients = [];


// ============================================================
// IMAGE PREVIEW
// ============================================================

if (imageUpload) {

    imageUpload.addEventListener(
        "change",
        function () {

            const file = this.files[0];

            if (!file) {
                return;
            }

            const reader = new FileReader();

            reader.onload = function (event) {

                previewImage.src =
                    event.target.result;

                previewSection.style.display =
                    "block";
            };

            reader.readAsDataURL(file);
        }
    );
}


// ============================================================
// ANALYZE IMAGE
// ============================================================

if (analyzeButton) {

    analyzeButton.addEventListener(
        "click",
        async function () {

            const file =
                imageUpload.files[0];

            if (!file) {

                alert(
                    "Please upload an image first."
                );

                return;
            }


            // Disable button

            analyzeButton.disabled = true;

            analyzeButton.textContent =
                "Reading label...";


            const formData =
                new FormData();

            formData.append(
                "image",
                file
            );


            try {

                const response =
                    await fetch(
                        "/analyze",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (!data.success) {

                    alert(
                        data.message ||
                        "Something went wrong."
                    );

                    return;
                }


                // Save extracted ingredients

                extractedIngredients =
                    data.ingredients || [];


                // Display ingredients

                displayIngredients(
                    extractedIngredients
                );


                // Show result sections

                resultSection.style.display =
                    "block";

                if (skinSection) {

                    skinSection.style.display =
                        "block";
                }

                if (analysisSection) {

                    analysisSection.style.display =
                        "block";
                }


                // Create question box

                createQuestionArea();


                // Scroll to ingredients

                resultSection.scrollIntoView({
                    behavior: "smooth"
                });

            }

            catch (error) {

                console.error(error);

                alert(
                    "Could not connect to the server."
                );
            }

            finally {

                analyzeButton.disabled =
                    false;

                analyzeButton.textContent =
                    "Analyze Product";
            }
        }
    );
}


// ============================================================
// DISPLAY INGREDIENTS
// ============================================================

function displayIngredients(
    ingredients
) {

    ingredientList.innerHTML = "";


    if (
        !ingredients ||
        ingredients.length === 0
    ) {

        ingredientList.innerHTML =
            "<p>No ingredients were detected.</p>";

        return;
    }


    ingredients.forEach(
        function (ingredient) {

            const span =
                document.createElement(
                    "span"
                );


            span.className =
                "ingredient";


            span.textContent =
                ingredient;


            // Click ingredient

            span.addEventListener(
                "click",
                function () {

                    askAboutIngredient(
                        ingredient
                    );
                }
            );


            ingredientList.appendChild(
                span
            );
        }
    );
}


// ============================================================
// CREATE QUESTION BOX
// ============================================================

function createQuestionArea() {

    // Remove old question box

    const oldBox =
        document.getElementById(
            "questionBox"
        );


    if (oldBox) {

        oldBox.remove();
    }


    const box =
        document.createElement(
            "div"
        );


    box.id =
        "questionBox";


    box.className =
        "question-box";


    box.innerHTML = `
        <h2>💬 Ask About an Ingredient</h2>

        <p>
            Click an ingredient above or ask your own question.
        </p>

        <div class="question-row">

            <input
                type="text"
                id="ingredientQuestion"
                placeholder="Example: What is Avobenzone?"
            >

            <button
                id="askButton"
                class="analyze-button"
            >
                Ask
            </button>

        </div>

        <div
            id="questionLoading"
            style="display:none;"
        >
            🔄 Analyzing...
        </div>
    `;


    analysisSection.parentNode.insertBefore(
        box,
        analysisSection
    );


    const askButton =
        document.getElementById(
            "askButton"
        );


    const questionInput =
        document.getElementById(
            "ingredientQuestion"
        );


    askButton.addEventListener(
        "click",
        function () {

            askQuestion();
        }
    );


    questionInput.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Enter"
            ) {

                askQuestion();
            }
        }
    );
}


// ============================================================
// ASK QUESTION ABOUT IMAGE INGREDIENT
// ============================================================

async function askQuestion() {

    const questionInput =
        document.getElementById(
            "ingredientQuestion"
        );


    const question =
        questionInput.value.trim();


    if (!question) {

        alert(
            "Please enter a question."
        );

        return;
    }


    const loading =
        document.getElementById(
            "questionLoading"
        );


    const askButton =
        document.getElementById(
            "askButton"
        );


    loading.style.display =
        "block";


    askButton.disabled =
        true;


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        ingredients:
                            extractedIngredients,

                        skin_type:
                            skinType.value ||
                            "Not specified"
                    })
                }
            );


        const data =
            await response.json();


        if (!data.success) {

            alert(
                data.message ||
                "Something went wrong."
            );

            return;
        }


        // Display AI answer

        displayAnswer(
            data.answer,
            data.ingredient
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not connect to the server."
        );
    }

    finally {

        loading.style.display =
            "none";

        askButton.disabled =
            false;
    }
}


// ============================================================
// ASK DIRECTLY BY CLICKING INGREDIENT
// ============================================================

function askAboutIngredient(
    ingredient
) {

    const questionInput =
        document.getElementById(
            "ingredientQuestion"
        );


    if (!questionInput) {

        return;
    }


    questionInput.value =
        `What is ${ingredient}?`;


    askQuestion();
}


// ============================================================
// DISPLAY AI ANSWER
// ============================================================

function displayAnswer(
    answer,
    ingredient
) {

    analysisResults.innerHTML = "";


    const answerCard =
        document.createElement(
            "div"
        );


    answerCard.className =
        "ingredient-card";


    answerCard.innerHTML =
        formatMarkdown(answer);


    analysisResults.appendChild(
        answerCard
    );


    analysisSection.style.display =
        "block";


    analysisSection.scrollIntoView({
        behavior: "smooth"
    });
}


// ============================================================
// MARKDOWN FORMATTER
// ============================================================

function formatMarkdown(
    text
) {

    if (!text) {

        return "";
    }


    let html = text;


    // Escape basic HTML

    html = html
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");


    // ### Heading

    html = html.replace(
        /^### (.*)$/gm,
        "<h3>$1</h3>"
    );


    // Bold text

    html = html.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    // Bullet points

    html = html.replace(
        /^- (.*)$/gm,
        "<li>$1</li>"
    );


    // Wrap consecutive list items

    html = html.replace(
        /((?:<li>.*<\/li>\s*)+)/g,
        "<ul>$1</ul>"
    );


    // Paragraph breaks

    html = html.replace(
        /\n\n+/g,
        "<br><br>"
    );


    // Single line breaks

    html = html.replace(
        /\n/g,
        "<br>"
    );


    return html;
}


// ============================================================
// MANUAL TEXT INGREDIENT ANALYSIS
// ============================================================

if (textAnalyzeButton) {

    textAnalyzeButton.addEventListener(
        "click",
        async function () {

            const text =
                ingredientInput.value.trim();


            if (!text) {

                alert(
                    "Please enter an ingredient."
                );

                return;
            }


            // Disable button

            textAnalyzeButton.disabled =
                true;

            textAnalyzeButton.innerText =
                "Analyzing...";


            // Show analysis section

            analysisSection.style.display =
                "block";


            analysisResults.innerHTML =
                "<p>🔍 Analyzing ingredient...</p>";


            try {

                const response =
                    await fetch(
                        "/analyze-text",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                ingredients:
                                    text
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!data.success) {

                    analysisResults.innerHTML =
                        `<p>${data.message || "Analysis failed."}</p>`;

                    return;
                }


                // Display formatted AI answer

                analysisResults.innerHTML =
                    formatMarkdown(
                        data.analysis
                    );


                // Scroll to answer

                analysisSection.scrollIntoView({
                    behavior: "smooth"
                });

            }

            catch (error) {

                console.error(
                    "TEXT ANALYSIS ERROR:",
                    error
                );


                analysisResults.innerHTML =
                    "<p>Could not connect to the server.</p>";
            }

            finally {

                textAnalyzeButton.disabled =
                    false;

                textAnalyzeButton.innerText =
                    "Analyze Ingredients";
            }
        }
    );
}
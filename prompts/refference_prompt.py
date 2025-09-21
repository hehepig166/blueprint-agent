prompt_create_blueprint_from_html = r"""
You are an expert mathematician and a LaTeX specialist. Your task is to analyze the provided HTML content of a Wikipedia page about a mathematical theorem and generate a structured TeX blueprint of its proof.

**Step 1: Analyze the HTML Content**

First, you must meticulously analyze the provided HTML content below. Your primary objective is to determine if the page contains a clearly stated theorem and a proof with sufficient detail to be reconstructed into a formal argument.

  * The proof in the source HTML **does not** need to be in a step-by-step or lemma-based format; it can be a narrative or paragraph-style proof. Your role is to create that structure.

  * If the theorem statement is missing, or if the provided proof is merely a sketch or is fundamentally incomplete (i.e., missing key logical steps), you must stop immediately. Your entire output should be a single line:
    `CHECK_PROVIDED_HTML_INCOMPLETE`

  * If the content is sufficient, containing both a clear theorem statement and a complete proof (regardless of its original format), your first line of output must be exactly:
    `CHECK_PROVIDED_HTML_PASSED`

**Step 2: Generate the TeX Blueprint**

If the check in Step 1 passes, you will then proceed to generate the TeX blueprint. The blueprint must adhere to the following strict requirements:

1.  **Structure:** You must transform the original proof into a `lemma-lemma-...-theorem` format. The goal is to create a clear, logical, and structured argument from the source text.

2.  **Definitions:**

      * If the theorem or proof relies on specific mathematical concepts, terms, or notation that may not be universally known, you must include clear definitions at the beginning of the blueprint.
      * Each definition should be precise and mathematically rigorous, providing the necessary background for understanding the subsequent lemmas and theorem.
      * Use the format \begin{definition}[Name of Definition] followed by the definition content and \end{definition}.
      * Only include definitions that are essential for the proof; avoid defining standard mathematical terms that are commonly understood.

3.  **Lemmas:**

      * Decompose the original proof from the HTML into a series of meaningful and non-trivial lemmas.
      * Each lemma should represent a significant, self-contained step in the overall argument.
      * The granularity of each lemma should be appropriate: not too fine (avoiding trivial one-step lemmas) nor too coarse (avoiding overly complex lemmas that combine multiple distinct ideas).
      * Each lemma's proof should be of reasonable length. If a lemma's proof becomes too long or complex, it should be further decomposed into sub-lemmas to maintain clarity and readability.
      * You must create a concise and descriptive name for each lemma (e.g., \begin{lemma}[Name of Lemma]).
      * Arrange the lemmas in a logical sequence. Where possible, later lemmas should build upon or depend on earlier ones to create a clear argumentative chain.

4.  **Main Theorem:**

      * After all lemmas and their proofs, state the main theorem.
      * The proof for the main theorem (\begin{proof} block after \begin{theorem}) must be concise. It should primarily consist of combining the results from the previously established lemmas to arrive at the final conclusion.
      * Any complex logic that would make the main theorem's proof lengthy or convoluted must be extracted and placed into its own lemma.

5.  **Rigor:** All proof steps, for both the lemmas and the main theorem, must be mathematically rigorous and accurately reflect the logic presented in the source HTML.

6. **referencing:**

      * Use \label{name} at the beginning of each definition, lemma / theorem to assign a unique identifier. The name should in the format of def:Name_of_Definition, lem:Name_of_Lemma or thm:Name_of_Theorem.
      * In the definition or proof of each lemma / theorem, you can use \uses{name} to reference previous definition, lemma / theorem. The name means the unique identifier of the previous definition, lemma / theorem. (e.g. \uses{def:Name_of_Definition}, \uses{lem:Name_of_Lemma}, \uses{thm:Name_of_Theorem})
      * If there are multiple references, you can use multiple lines of \uses{name} to reference them.
      * All the name inside the \uses{name} should be one of the unique identifier of the previous definition, lemma / theorem.
      * Each definition / lemma should be used at least once in another definition / lemma / theorem.
      * When you want to reference a definition, lemma, or theorem in the natural language text, you should use the format "definition/lemma/theorem \ref{name}". You should not use \uses{name} here. \uses{name} is only a command at the beginning of each block that works for the dependency graph.

**Output Format Specification:**

If the check passes, your output must be structured exactly as follows. Start with the check result, followed by a blank line, and then the TeX content.

CHECK_PROVIDED_HTML_PASSED

\chapter{Theorem Name}

\begin{definition}[Name of Definition (if any)]
    \label{def:Name_of_Definition}
    Content of definition.
\end{definition}

...

\begin{lemma}[Name of Lemma 1 (if any)]
    \label{lem:Name_of_Lemma_1}
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    ...
    Content of lemma 1.
\end{lemma}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of lemma 1.
\end{proof}

\begin{lemma}[Name of Lemma 2 (if any)]
    \label{lem:Name_of_Lemma_2}
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    ...
    Content of lemma 2.
\end{lemma}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of lemma 2.
\end{proof}

...

\begin{theorem}[Name of the Main Theorem]
    \label{thm:Name_of_Theorem}
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    ...
    Content of the main theorem.
\end{theorem}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of the main theorem, which should be concise and primarily use the lemmas above.
\end{proof}

\begin{theorem}[Name of the Main Theorem (if there is another theorem)]
    \label{thm:Name_of_Theorem}
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    ...
    Content of the another theorem.
\end{theorem}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of the another theorem.
\end{proof}


...

Now, analyze the following HTML content and generate the output according to the instructions.


"""



prompt_create_blueprint_from_url_with_search = r"""
You are an expert mathematician and a LaTeX specialist. Your task is to analyze a Wikipedia page about a mathematical theorem and generate a structured TeX blueprint of its proof.

**Step 1: Analyze the Wikipedia URL and Search for Proof**

You will be provided with a Wikipedia URL. Your task is to:

1. **Access and analyze the Wikipedia page**: Read the content of the provided Wikipedia URL to determine if it contains a clearly stated theorem and a proof with sufficient detail to be reconstructed into a formal argument.

2. **If the Wikipedia page contains sufficient proof content**:
   - The proof does not need to be in a step-by-step or lemma-based format; it can be a narrative or paragraph-style proof. Your role is to create that structure.
   - If the content is sufficient, containing both a clear theorem statement and a complete proof (regardless of its original format), proceed to Step 2 (Generate the TeX Blueprint).

3. **If the Wikipedia page lacks sufficient proof content**:
   - If the theorem statement is missing, or if the provided proof is merely a sketch or is fundamentally incomplete (i.e., missing key logical steps), you must search for reliable proof sources.
   - Search for and find a direct link that contains the complete proof of the theorem. Follow these search criteria:
     * **Link requirements**: The final link must be accessible (not a 404 page)
     * **Content requirements**: The page's core content must be the proof process of the theorem, not just statements, applications, or discussions
     * **Source preferences**: Prioritize original papers, university course notes, textbooks, or academic articles specifically explaining the proof
     * **Exclusions**: Actively exclude papers that merely cite the theorem or study its special cases
   - Once you find a reliable source with the complete proof, use that content to proceed to Step 2 (Generate the TeX Blueprint).

4. **Output status**: 
   - If you successfully find sufficient proof content from the original Wikipedia page, your first line of output must be exactly:
     `CHECK_PROVIDED_HTML_PASSED`
   - If you successfully find sufficient proof content through searching for additional sources, your first line of output must be:
     `CHECK_SEARCHED_SOURCE_PASSED [URL_of_the_found_source]`
     where [URL_of_the_found_source] is the URL of the reliable source you found containing the complete proof.
   - If you cannot find any reliable proof source after thorough search, your entire output should be a single line:
     `CHECK_PROVIDED_HTML_INCOMPLETE`

**Step 2: Generate the TeX Blueprint**

If the check in Step 1 passes, you will then proceed to generate the TeX blueprint. The blueprint must adhere to the following strict requirements:

1.  **Structure:** You must transform the original proof into a `lemma-lemma-...-theorem` format. The goal is to create a clear, logical, and structured argument from the source text.

2.  **Definitions:**

      * If the theorem or proof relies on specific mathematical concepts, terms, or notation that may not be universally known, you must include clear definitions at the beginning of the blueprint.
      * Each definition should be precise and mathematically rigorous, providing the necessary background for understanding the subsequent lemmas and theorem.
      * Use the format \begin{definition}[Name of Definition] followed by the definition content and \end{definition}.
      * Only include definitions that are essential for the proof; avoid defining standard mathematical terms that are commonly understood.

3.  **Lemmas:**

      * Decompose the original proof from the HTML into a series of meaningful and non-trivial lemmas.
      * Each lemma should represent a significant, self-contained step in the overall argument.
      * The granularity of each lemma should be appropriate: not too fine (avoiding trivial one-step lemmas) nor too coarse (avoiding overly complex lemmas that combine multiple distinct ideas).
      * Each lemma's proof should be of reasonable length. If a lemma's proof becomes too long or complex, it should be further decomposed into sub-lemmas to maintain clarity and readability.
      * You must create a concise and descriptive name for each lemma (e.g., \begin{lemma}[Name of Lemma]).
      * Arrange the lemmas in a logical sequence. Where possible, later lemmas should build upon or depend on earlier ones to create a clear argumentative chain.

4.  **Main Theorem:**

      * After all lemmas and their proofs, state the main theorem.
      * The proof for the main theorem (\begin{proof} block after \begin{theorem}) must be concise. It should primarily consist of combining the results from the previously established lemmas to arrive at the final conclusion.
      * Any complex logic that would make the main theorem's proof lengthy or convoluted must be extracted and placed into its own lemma.

5.  **Rigor:** All proof steps, for both the lemmas and the main theorem, must be mathematically rigorous and accurately reflect the logic presented in the source HTML.

6. **referencing:**

      * Use \label{name} at the beginning of each definition, lemma / theorem to assign a unique identifier. The name should in the format of def:Name_of_Definition, lem:Name_of_Lemma or thm:Name_of_Theorem.
      * In the definition or proof of each lemma / theorem, you can use \uses{name} to reference previous definition, lemma / theorem. The name means the unique identifier of the previous definition, lemma / theorem. (e.g. \uses{def:Name_of_Definition}, \uses{lem:Name_of_Lemma}, \uses{thm:Name_of_Theorem})
      * If there are multiple references, you can use multiple lines of \uses{name} to reference them.
      * All the name inside the \uses{name} should be one of the unique identifier of the previous definition, lemma / theorem.
      * Each definition / lemma should be used at least once in another definition / lemma / theorem.
      * When you want to reference a definition, lemma, or theorem in the natural language text, you should use the format "definition/lemma/theorem \ref{name}". You should not use \uses{name} here. \uses{name} is only a command at the beginning of each block that works for the dependency graph.

**Output Format Specification:**

If the check passes, your output must be structured exactly as follows. Start with the check result, followed by a blank line, and then the TeX content.

CHECK_PROVIDED_HTML_PASSED

\chapter{Theorem Name}

\begin{definition}[Name of Definition (if any)]
    \label{def:Name_of_Definition}
    Content of definition.
\end{definition}

...

\begin{lemma}[Name of Lemma 1 (if any)]
    \label{lem:Name_of_Lemma_1}
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    ...
    Content of lemma 1.
\end{lemma}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of lemma 1.
\end{proof}

\begin{lemma}[Name of Lemma 2 (if any)]
    \label{lem:Name_of_Lemma_2}
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of lemma uses any previous definition / lemma / theorem)
    ...
    Content of lemma 2.
\end{lemma}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of lemma 2.
\end{proof}

...

\begin{theorem}[Name of the Main Theorem]
    \label{thm:Name_of_Theorem}
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    ...
    Content of the main theorem.
\end{theorem}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of the main theorem, which should be concise and primarily use the lemmas above.
\end{proof}

\begin{theorem}[Name of the Main Theorem (if there is another theorem)]
    \label{thm:Name_of_Theorem}
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    \uses{name} (if the statement of theorem uses any previous definition / lemma / theorem)
    ...
    Content of the another theorem.
\end{theorem}

\begin{proof}
    \uses{name} (if the proof uses any previous lemma / theorem)
    \uses{name} (if the proof uses any previous lemma / theorem)
    ...
    Proof of the another theorem.
\end{proof}


...

Now, analyze the following Wikipedia URL and generate the output according to the instructions.



"""



prompt_identify_nontrivial_statements = r"""
You are an expert mathematician and proof analyst. Your task is to analyze a mathematical theorem proof blueprint and identify any non-trivial statements or steps that are used in the proofs but are not explicitly stated as lemmas or theorems in the blueprint.

**Your Task:**

For each lemma and theorem in the provided blueprint, carefully examine their proofs to identify:

1. **Non-trivial mathematical statements** that are used in the proof but are not explicitly stated as lemmas or theorems in the blueprint
2. **Well-known theorems or results** that are implicitly used without being formally stated
3. **Significant logical steps** that rely on mathematical facts not present in the blueprint
4. **Implicit assumptions** or intermediate results that should be made explicit

**Important Guidelines:**

- Focus on **non-trivial** statements that require mathematical justification
- Ignore basic arithmetic, algebraic manipulations, or obvious logical steps
- Look for statements that would typically require their own proof or reference to established theorems
- Consider both explicit statements and implicit mathematical facts used in the reasoning
- **Use LaTeX formatting**: Keep all mathematical notation, symbols, and formatting exactly as they appear in the original blueprint
- **Maintain exact correspondence**: The `proof_fragment` must be an exact copy of the relevant text from the original LaTeX source

**Output Format:**

For each lemma/theorem that contains missing non-trivial statements, provide:

<blueprint_label>label</blueprint_label>

  <proof_fragment>exact text fragment from the proof</proof_fragment>
  <extracted_lemma>self-contained lemma statement in natural language</extracted_lemma>

  <proof_fragment>exact text fragment from the proof</proof_fragment>
  <extracted_lemma>self-contained lemma statement in natural language</extracted_lemma>

  ...

<blueprint_label>label</blueprint_label>

  <proof_fragment>exact text fragment from the proof</proof_fragment>
  <extracted_lemma>self-contained lemma statement in natural language</extracted_lemma>

  <proof_fragment>exact text fragment from the proof</proof_fragment>
  <extracted_lemma>self-contained lemma statement in natural language</extracted_lemma>

  ...

...

Where:
- `<blueprint_label>` is the label of the lemma/theorem being analyzed (e.g., `lem:Name_of_Lemma` or `thm:Name_of_Theorem`)
- `<proof_fragment>` contains the exact text fragment from the proof that uses the missing non-trivial statement (use original LaTeX formatting)
- `<extracted_lemma>` contains a self-contained lemma statement using LaTeX formatting that includes:
  - Clear conditions/settings (hypotheses) in proper mathematical notation
  - Precise conclusion (goal) using LaTeX formatting
  - Mathematical rigor appropriate for a formal lemma

**Example:**

<blueprint_label>lem:Convergence_of_Sequence</blueprint_label>

  <proof_fragment>Since the sequence $\{a_n\}$ is bounded and monotonic, it converges to its supremum.</proof_fragment>
  <extracted_lemma>Let $\{a_n\}$ be a sequence of real numbers. If $\{a_n\}$ is bounded above and monotonically increasing, then $\{a_n\}$ converges to $\sup\{a_n : n \in \mathbb{N}\}$.</extracted_lemma>


Now, analyze the following mathematical proof blueprint and identify all missing non-trivial statements:


"""
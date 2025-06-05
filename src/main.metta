; src/main.metta
;   1. Register our python module (scripts/call_llms and scripts/write_to_file)
;   2. Import raw data (data/nodes.metta)
;   3. Import the llm_operations atom
;   4. Defines a single rule (summarize-gene) that:
;       Matches each (gene $GID) and its attributes
;       Build a list of fields
;       calls call_llm $summary
;       calls write_to_file with list_of_fields, summary, outputs_file


; Python atom - use absolute path
!(register-module! "/home/liulj/MeTTa-Project/src")

; Register the data folder (where nodes.metta lives)
!(register-module! "/home/liulj/MeTTa-Project/data")

; Load raw data
!(import &self data:nodes)

;Sanity check: do we see any (gene $GID) atoms?
!(print "Checking data loading…")
!(match &self (gene $GID) (print "Found gene: " $GID))

; Load our Python operations (call_llm and write_to_file)
!(import &self llm_operations)

; Define a helper to collect all the attributes for a given $GID
(= (collect-fields $GID)
    ; We'll build a MeTTa list [GID, Name, Type, Chr, Start, End, SynList]
    (list
        $GID
        (match &self (gene_name (gene $GID) $Name) $Name)
        (match &self (gene_type (gene $GID) $Type) $Type)
        (match &self (chr (gene $GID) $Chr) $Chr)
        (match &self (start (gene $GID) $Start) $Start)
        (match &self (end   (gene $GID) $End)   $End)
        (match &self (synonyms (gene $GID) $SynList) $SynList)
    )
)

; The main "top-level" rule: for every gene, summarize and write to file
(= (summarize-gene)
   (begin
        ; For each gene ID we find in the space...
        (match &self (gene $GID)
            ; Collect the fields in a list
            (let $Fields (collect-fields $GID)
                ; Call the LLM to get a summary (a string)
                (let $Summary (call_llm $Fields)
                    ; Write the original info + summary into a file
                    (write_to_file $Fields $Summary "output/summaries.txt" "text")
                    ; Return the summary so we can see it in REPL if desired
                    $Summary
                )
            )
        )
    )
)

; Execute the summarization
!(summarize-gene)


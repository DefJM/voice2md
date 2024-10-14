import ollama


def llm_summarize_transcript(client, transcript, model="llama3.2:1b"):

    few_shots = """

    <example>
    <voice memo>"more this is a cool set up the four most dangerous words in investing is this time is different the twelve most dangerous words in investing is the four most dangerous words in investing is this time is different interesting"</voice memo>
    <tldr_summary>"The four most dangerous words in investing are 'this time is different'."</tldr_summary>
    </example>

    <example>
    <voice memo>"I am reading from the Wiki article about taxation in Germany. Taxes in Germany are levied at various government levels, the federal government, the 16 states and numerous municipalities. The structured tax system has evolved significantly since the reunification of Germany in 1990 and the integration within the European Union, which has influenced tax policies. Today, income tax and valued added tax, VAT, are the primary sources of tax revenue. These taxes reflect Germany's commitment to a balanced approach between direct and indirect taxation, essentially for funding extensive social welfare programs and public infrastructure. The modern German tax system accentuate on fairness and efficiency, adapting to global economic trends and domestic fiscal needs."</voice memo>
    <tldr_summary>"Germany's tax system operates at federal, state, and local levels, with income tax and VAT as primary revenue sources. It aims for fairness and efficiency while funding social programs and adapting to economic trends."</tldr_summary>
    </example>

    <example>
    <voice memo>"Ich lese aus der Wiki vor und zwar über die Einkommenssteuer. Die Einkommenssteuer in Deutschland, Abkürzung EST, ist eine Gemeinschaftssteuer, die auf das Einkommen natürlicher Personen erhoben wird. Rechtsgrundlage für die Berechnung und Erhebung der Einkommenssteuer ist, neben weiteren Gesetzen, das Einkommenssteuergesetz, in Klammern ESTG. Der Einkommenssteuertarif regelt die Berechnungsvorschriften. Bemessungsgrundlage ist das zu versteuernde Einkommen. Im Jahr 2021 nahm der deutsche Staat rund 290 Milliarden Euro Lohn- und Einkommenssteuer ein. Das entspricht über einem Drittel der gesamten Steuereinnahmen Deutschlands. Der ebenfalls vorkommende Ausdruck Einkommenssteuer mit Fugen S wird in der juristischen Fachsprache nicht verwendet. Allgemeines Erhebungsformen der Einkommenssteuer sind die Lohnsteuer, die Kapitalertragsteuer, die Bauabzugsteuer und die Aufsichtsratsteuer. Sie werden auch als Quellensteuersteuern bezeichnet, da sie direkt an der Quelle abgezogen werden. Die Abgeltungssteuer dient seit 2009 als bestimmte Anwendung der Kapitalertragsteuer. Nach dem Welteinkommensprinzip sind die in Deutschland Steuerpflichtigen mit ihrem weltweiten Einkommen steuerpflichtig."</voice memo>
    <tldr_summary>"Income tax in Germany is a major source of government revenue, accounting for over a third of total tax income. It's levied on individuals' worldwide income and collected through various forms including wage tax, capital gains tax, and withholding taxes."</tldr_summary>
    </example>
    """

    system_message = f"""
    You task is to summarize raw transcripts of voice memos, which can be 
    lengthy, unstructured and can even contain errors. Here are some examples
    of how you should format your response.
    {few_shots}

    Your task is to summarize the following voice memo in a concise and structured manner. 
    The recording will be in English or in German. Provide a summary in English.
    Be short and precise. No yabbering. Don't invent stuff. At maximum, this can 
    be two sentences. Summarize what you can understand from the content of the 
    following voice memo. 
    Don't add any explanations or whatsoever. Your response is used as a summary 
    only and should be between <tldr_summary> and </tldr_summary> tags. 
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Voice memo: {transcript['text']}"},
        ],
    )

    return response


# TODO: move these private examples to a separate file in ~/data/raw
def llm_generate_note_title(client, transcript, model="llama3.2:1b"):

    few_shots = """

    <example>
    <voice memo>"more this is a cool set up the four most dangerous words in investing is this time is different the twelve most dangerous words in investing is the four most dangerous words in investing is this time is different interesting"</voice memo>
    <title>"The four most dangerous words in investing"</title>
    </example>

    <example>
    <voice memo>"I am reading from the Wiki article about taxation in Germany. Taxes in Germany are levied at various government levels, the federal government, the 16 states and numerous municipalities. The structured tax system has evolved significantly since the reunification of Germany in 1990 and the integration within the European Union, which has influenced tax policies. Today, income tax and valued added tax, VAT, are the primary sources of tax revenue. These taxes reflect Germany's commitment to a balanced approach between direct and indirect taxation, essentially for funding extensive social welfare programs and public infrastructure. The modern German tax system accentuate on fairness and efficiency, adapting to global economic trends and domestic fiscal needs."</voice memo>
    <title>"Taxation in Germany"</title>
    </example>

    <example>
    <voice memo>"Ich lese aus der Wiki vor und zwar über die Einkommenssteuer. Die Einkommenssteuer in Deutschland, Abkürzung EST, ist eine Gemeinschaftssteuer, die auf das Einkommen natürlicher Personen erhoben wird. Rechtsgrundlage für die Berechnung und Erhebung der Einkommenssteuer ist, neben weiteren Gesetzen, das Einkommenssteuergesetz, in Klammern ESTG. Der Einkommenssteuertarif regelt die Berechnungsvorschriften. Bemessungsgrundlage ist das zu versteuernde Einkommen. Im Jahr 2021 nahm der deutsche Staat rund 290 Milliarden Euro Lohn- und Einkommenssteuer ein. Das entspricht über einem Drittel der gesamten Steuereinnahmen Deutschlands. Der ebenfalls vorkommende Ausdruck Einkommenssteuer mit Fugen S wird in der juristischen Fachsprache nicht verwendet. Allgemeines Erhebungsformen der Einkommenssteuer sind die Lohnsteuer, die Kapitalertragsteuer, die Bauabzugsteuer und die Aufsichtsratsteuer. Sie werden auch als Quellensteuersteuern bezeichnet, da sie direkt an der Quelle abgezogen werden. Die Abgeltungssteuer dient seit 2009 als bestimmte Anwendung der Kapitalertragsteuer. Nach dem Welteinkommensprinzip sind die in Deutschland Steuerpflichtigen mit ihrem weltweiten Einkommen steuerpflichtig."</voice memo>
    <title>"Income Tax in Germany"</title>
    </example>
    """

    system_message = f"""
    Your task is to provide a fitting short note title for a raw transcripts of 
    voice memos, which can be lengthy, unstructured and sometimes even contain errors. 
    Here are some examples of raw transcripts and a fitting title for each.

    {few_shots}

    
    The recording will be in English or in German. Provide a note title in English.
    Be short, max 5 words. No yabbering. Don't invent stuff. 
    Just a title without special letters for the user's voice memo content. 
    Don't add any explanations or whatsoever. Your response is used as a title only 
    and should be between <title> and </title> tags. 
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Voice memo: {transcript['text']}"},
        ],
    )

    return response
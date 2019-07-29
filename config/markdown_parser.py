
def mrkdwn_to_slack(markdown_text):

    #convert line-break
    markdown_text = markdown_text.split()
    for i in range(len(markdown_text)):
        if markdown_text[i] == '<br>':
            markdown_text[i] = '\n'
    markdown_text = ' '.join(markdown_text)
    markdown_text = list(markdown_text)

    # convert links
    for i in range(len(markdown_text)):
        if markdown_text[i] == '(':
            markdown_text[i] = '<'
        if markdown_text[i] == ')':
            markdown_text[i] ='>'
        if markdown_text[i] == '[':
            while markdown_text[i] != ']':
                markdown_text[i]=""
                i+= 1
            markdown_text[i] = ""

    return ''.join(markdown_text)


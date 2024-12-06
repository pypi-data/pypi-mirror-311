#!/usr/bin/env python

import logging


########################################################################################################################


class SlackApp(object):
    """Create Slack App payloads from a title header and a body.

    The title heading will be formatted as bold, and the body will be formatted as Code block.
    If the payload is too large it will be split into multiple parts - individual posts.
    If spilt, the provided heading will be used for all posts, but the part number will be appended to the heading.


    Attributes
    ----------
    title : str
        The title of the Slack message
    content : str
        The report summary. Only used it the split_msg() method has to be called.
        The report. Only used it the split_msg() method has to be called.
        The report and summary combined. Used as default if the split_msg() does not have to be called.
    max_chars : int
        Count of characters for when the Slack message is considered too long and will be split into multiple messages
        (default: 2500)

    Methods
    -------
    get_payloads()
    split_msg()
        Splits long messages into multiple parts - to be posted to Slack individually
        If splitting up a message to a Slack App, each message will be a payload in the following format:
        {"text": "formatted message"}
    """

    def __init__(self, title, content, max_chars=2500):
        """
        Parameters
        ----------
        title : str
            The title of the Slack message
        content : str
            The message body
        max_chars : int
            Count of characters for when the Slack message is considered too long and will be split
            into multiple messages
            (default: 2500)
        """

        self.title = title
        self.content = content
        self.max_chars = max_chars

    def get_payloads(self):
        """Slack formats the header as bold and the body as code block

        Calls the split_msg method if needed to split the message to multiple posts

        Returns
        -------
        payloads : list
            A list of slack payloads.
        """

        # Building payloads for Slack app
        logging.info("Building payload for Slack App..")
        payloads = [{"text": f"*{self.title}*\n```{self.content}```"}]

        # If the payload is too large for the Slack App it will be split into multiple posts
        if len(str(payloads)) > self.max_chars:
            logging.info("The message will be to large. Splitting up into chunks..")
            payloads = self.split_msg()

        logging.info(f"{len(payloads)} slack app payloads created. ")

        return payloads

    def split_msg(self):
        """splits long messages into multiple parts - to be posted to Slack individually

        Returns
        -------
        results : list
            The list of the split messages as dicts
        """

        results = []

        cb = "```"

        # Then the report is split into chucks
        report_lines = self.content.splitlines()

        # The two first lines of the report is the header, which will be used in every part
        header = f"{cb}{report_lines.pop(0)}\n{report_lines.pop(0)}\n"

        # The first part of the first report payload / txt is initialized
        part = 1
        txt = ""
        payload = {"text": f"*{self.title} - Part {part}*\n{header}"}

        # Parse through every line of data in the report and add it to individual payloads / txt
        for line in report_lines:
            if len(txt) <= self.max_chars:
                txt += f"{line}\n"
                payload["text"] += f"{line}\n"
            else:
                # When a payload / txt have reacted it's max size it is added to the list of results
                payload["text"] += cb
                results.append(payload)

                # Then a new payload / txt is initialized
                part += 1
                txt = f"{line}\n"
                payload = {"text": f"*{self.title} - Part {part}*\n{header}{txt}"}

        # If a remaining payload / txt exists, then it will also be added to the list of payloads
        if txt:
            payload["text"] += cb
            results.append(payload)

        logging.info(f"Message was split into {len(results)} chunks.")

        return results


class MSTeamsPayload(object):
    """Build a default MS Teams payload. Uses the provided 'title', 'text' and 'summary'.
    The text may be a html table.
    The summary is a dict where the key/value pairs name 'text'/'value' will be used to as facts in the payload.


    Attributes
    ----------
    title : str
        The title of the MS Teams message
    text : str
        The text of the MS Teams message, e.g. a html table
    summary : dict
        The dict which populates the 'facts'
    facts : list
        The list of facts which will be populated by the provided summary


    Methods
    -------
    set_json_facts()
        Parse the summary dict values. If any values contain a dict with a 'text' key it will be added to the list of
        dicts in the facts list. 'name': value of 'text'. 'value': value of 'value'.
    get_facts()
        Returns the list of facts
    get_json_output()
        Build a default MS Teams payload. Uses the provided 'title', 'text' and 'summary'. The 'text' dicts of the
        'summary' makes up the facts.
    """

    def __init__(self, title, text, summary=None):
        """
        Parameters
        ----------
        title : str
            The 'activityTitle' which is the title of the message in MS Teams
        text : str
            The text to be added below the 'facts'. The 'text' may be in html format.
        summary : dict
            The summary part of the config which will make upt the 'facts'.
        """

        self.title = str(title)
        self.text = str(text)
        self.summary = summary
        self.facts = []

    def set_json_facts(self):
        """generates the fact used in the json output for MS Teams"""

        if not isinstance(self.summary, dict):
            return

        self.facts = []
        for k, v in self.summary.items():
            self.facts.append({"name": str(k),
                               "value": str(v)
                               })

    def get_facts(self):
        return self.facts

    def get_payload(self):
        """add the facts and text to the json output for MS Teams, and then return the json output

        Returns
        -------
        dict
            The payload as dict. If not fact are provided, then None is returned.
        """

        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "-",
            "sections": [
                {
                    "activityTitle": self.title,
                    "activitySubtitle": "",
                    "activityImage": "",
                    "facts": [],
                    "markdown": True
                },
                {
                    "startGroup": True,
                    "text": ""
                }
            ]
        }

        payload["sections"][0]["facts"] = self.facts
        payload["sections"][1]["text"] = self.text

        return payload

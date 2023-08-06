# -*- coding: utf-8 -*-

DESCRIPTION = """Make edits to Markdown docs, prioritizing making sure nothing is lost from original."""

from collections import OrderedDict
from typing import Any, Generator, List, Tuple
import difflib
import re

import logging

root_logger = logging.getLogger()
logger = root_logger.getChild(__name__)

# match (english-language) hashtags between 1 and 30 characters long
# https://stackoverflow.com/questions/42065872/regex-for-a-valid-hashtag
pattern_hashtag = re.compile(r"(^|\B)#(?![0-9_]+\b)([a-zA-Z0-9_]{1,30})(\b|\r)")


class MarkdownDoc:
    def __init__(
        self,
        txt: str,
        parent: Any = None,
        level=0,
    ) -> None:
        # self.txt = txt
        self.parent = parent
        self.level = level

        self.sections = []
        lines = txt.split("\n")
        if any([line.startswith("#") for line in lines[1:]]):
            for title, sec in self.split_into_sections(txt, level=level + 1):
                if not title:
                    break
                self.sections.append(
                    MarkdownSection(sec, title, parent=self, level=level + 1)
                )
        # self.sections = [
        #     MarkdownSection(sec, title, parent=self, level=level+1)
        #     for title, sec in self.split_into_sections(txt, level=level+1)
        # ]

    @property
    def txt(self):
        all_lines = []
        for section in self.sections:
            all_lines = all_lines + section.lines
        return "\n".join(all_lines)

    def __repr__(self) -> str:
        txt_repr = self.txt[:50] + "..." if len(self.txt) > 50 else self.txt
        txt_repr = txt_repr.replace("\n", "\\")
        return f"{self.__class__}({txt_repr})"

    def get_sections_by_level(self, level=2):
        return [sec for sec in self.traverse() if sec.level == level]

    def get_section_by_title(self, title: str) -> "MarkdownSection":
        s = [sec for sec in self.traverse() if sec.level > 0 and sec.title.lower() == title.lower()]
        if len(s) < 1:
            raise KeyError(f"could not find section with title {title}")
        elif len(s) > 1:
            raise KeyError(f"ERROR: more than one section found with title {title}")
        return s[0]

    def split_into_sections(
        self, markdown_text: str, level=2
    ) -> Generator[Tuple[str, List[str]], None, None]:
        """This is a very simple way of splitting the markdown text into sections.
        It will not handle edge cases very well.

        Args:
            markdown_text (str): full text in Markdown format
            level (int, optional): Heading level to split by. Defaults to 2, meaning "## <Heading label>"

        Yields:
            Generator[Tuple[str, List[str]], None, None]: Tuple of (section title, list of lines)
        """
        heading_indicator = "#" * level
        protect_flag = False
        # sections = OrderedDict()
        this_section = []
        this_section_title = ""
        # this_section_txt = ""
        for line in markdown_text.split("\n"):
            if line.startswith("```"):
                protect_flag = not protect_flag
            if protect_flag is False and line.startswith(heading_indicator + " "):
                # sections.append("\n".join(this_section))
                # sections[this_section_title] = "\n".join(this_section)
                # this_section_txt = "\n".join(this_section)
                if this_section_title:
                    yield this_section_title, this_section
                this_section = [line]
                this_section_title = line.strip(heading_indicator).strip()
            else:
                this_section.append(line)
        # sections.append("\n".join(this_section))
        # this_section_txt = "\n".join(this_section)
        yield this_section_title, this_section

    # def refresh_all_sections(self):
    #     for sec in self.sections:
    #         sec.refresh()

    def traverse(self, hist=None):
        if hist is None:
            hist = [self]
        else:
            hist.append(self)
        if self.sections:
            for sec in self.sections:
                hist = sec.traverse(hist)
        return hist


class MarkdownSection(MarkdownDoc):
    def __init__(
        self, lines: List[str], title: str = "", parent: Any = None, level=2
    ) -> None:
        self.lines = lines
        self.title = title
        self.parent = parent
        self.level = level
        super().__init__("\n".join(self.lines), level=self.level, parent=self.parent)

    @property
    def content(self) -> str:
        return self.get_content()

    def get_content(self) -> str:
        content_lines = self.lines[1:]
        content = "\n".join(content_lines)
        content = content.strip()
        return content

    def __repr__(self) -> str:
        txt_repr = self.txt[:50] + "..." if len(self.txt) > 50 else self.txt
        txt_repr = txt_repr.replace("\n", "\\")
        return f"{self.__class__}({txt_repr})"

    def __str__(self) -> str:
        return self.txt

    def refresh(self) -> None:
        super().__init__("\n".join(self.lines), level=self.level, parent=self.parent)

    def get_resource_ids(self) -> List[str]:
        # example of a resource id:
        # "![](:/f04c1849b3e64b5ca151a737720s0132)"
        return re.findall(r"!\[.*?\]\(:/([a-zA-Z0-9]+?)\)", self.content)

    def update(self, new_txt: str, force: bool = False) -> str:
        new_sec = MarkdownSection(new_txt.split("\n"))
        if not new_sec.content or new_sec.content == "None":
            # no new text to replace. do nothing
            return "no update"
        if self.txt == new_txt:
            # new text is the same as old text. do nothing
            return "no update"

        if force is True:
            replace = True
        else:
            replace = False
            if not self.content or self.content == "None":
                # no old text exists. safe to replace
                replace = True
            else:
                s = difflib.SequenceMatcher(
                    None, self.content.splitlines(), new_sec.content.splitlines()
                )
                tags = [opcode[0] for opcode in s.get_opcodes()]
                if all(tag in ["equal", "insert"] for tag in tags):
                    # no merge conflicts (no lines are marked to delete or replace). safe to replace old text with new text
                    replace = True
                else:
                    logger.debug(tags)
        if replace is True:
            # self.txt = new_txt
            self.lines = new_txt.split("\n")
            # self.content = self.get_content()
            self.refresh()
            return "updated"

        logger.debug(new_txt)
        from difflib import Differ

        logger.debug(MarkdownSection(new_txt.splitlines()).content)
        for x in Differ().compare(self.lines, new_txt.splitlines()):
            logger.debug(x)
        raise RuntimeError("could not update text")

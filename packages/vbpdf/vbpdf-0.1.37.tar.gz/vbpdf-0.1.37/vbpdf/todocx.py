
import click
import os
import sys
from rich.console import Console
from .topng import topng
from docx import Document
from docx.shared import Inches


@click.command(
        help="Converts pdf into docx file."
        )
@click.option(
        '-i',
        '--inputfile',
        type=click.Path(),
        default="./main.pdf",
        show_default=True,
        help="Input file name"
        )
@click.option(
        '-r',
        '--ranges',
        nargs=2,
        default=([1, 1]),
        type=click.Tuple([int, int]),
        show_default=True,
        help="Page range to be converted into png"
        )
@click.pass_context
def todocx(ctx, inputfile, ranges):

    doc = Document()
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0)
        s.left_margin = Inches(0)
        s.right_margin = Inches(0)
        s.bottom_margin = Inches(0)

    for i in range(ranges[0], ranges[1]+1):
        ctx.invoke(topng, inputfile=inputfile, ranges=(i, i), transparent=True, dpi=320)
        
        click.secho(f'\n')

    for i in range(ranges[0], ranges[1]+1):
        doc.add_picture(f'main-{i}.png', width=Inches(8.7), height=Inches(11.2))
        doc.add_page_break()
        os.remove(f'main-{i}.png')
    

    doc.save(f'main.docx')

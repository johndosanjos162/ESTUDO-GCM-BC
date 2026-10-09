"""Geração de PDF — Caderno de Questões (com suporte a UTF-8)."""

from io import BytesIO
from datetime import datetime
import html
import json
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ============================================================
# FONTE UNICODE (para acentos funcionarem corretamente)
# ============================================================

_FONT_NAME = "Helvetica"
_FONT_BOLD = "Helvetica-Bold"


def _registrar_fonte_unicode():
    """
    Tenta registrar uma fonte Unicode.
    Se não encontrar, usa Helvetica (que suporta Latin-1).
    """
    global _FONT_NAME, _FONT_BOLD

    # Caminhos comuns de fontes DejaVu em sistemas Linux/Mac
    caminhos = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/DejaVuSans.ttf",
        "C:/Windows/Fonts/DejaVuSans.ttf",
    ]

    regular = None
    bold = None

    for c in caminhos:
        if os.path.exists(c):
            if "Bold" in c and not bold:
                bold = c
            elif not regular:
                regular = c

    if regular:
        try:
            pdfmetrics.registerFont(TTFont("DejaVu", regular))
            _FONT_NAME = "DejaVu"
        except Exception as e:
            print(f"[aviso] Não foi possível registrar DejaVu: {e}")

    if bold:
        try:
            pdfmetrics.registerFont(TTFont("DejaVu-Bold", bold))
            _FONT_BOLD = "DejaVu-Bold"
        except Exception:
            _FONT_BOLD = _FONT_NAME


_registrar_fonte_unicode()


# ============================================================
# HELPERS
# ============================================================

def _esc(texto) -> str:
    """Escapa texto com segurança para o Paragraph."""
    if texto is None:
        return ""
    if isinstance(texto, bytes):
        try:
            texto = texto.decode("utf-8")
        except Exception:
            texto = texto.decode("latin-1", errors="ignore")
    texto = str(texto)
    texto = texto.replace("\n", "<br/>")
    return html.escape(texto).replace("&lt;br/&gt;", "<br/>")


def _parse_alts(valor) -> list:
    if isinstance(valor, str):
        try:
            return json.loads(valor)
        except Exception:
            return []
    return valor or []


# ============================================================
# GERADOR DE PDF
# ============================================================

def gerar_caderno_pdf(
    questoes_por_bloco: dict,
    incluir_gabarito: bool = True,
    incluir_explicacao: bool = False,
    titulo: str = "Caderno de Questões",
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title=titulo, author="Estudos GMBC",
    )

    styles = getSampleStyleSheet()

    st_titulo = ParagraphStyle(
        "TituloCustom", parent=styles["Title"],
        fontName=_FONT_BOLD,
        fontSize=24, textColor=HexColor("#1e3a5f"),
        spaceAfter=12, alignment=TA_CENTER,
    )
    st_sub = ParagraphStyle(
        "SubCustom", parent=styles["Normal"],
        fontName=_FONT_NAME,
        fontSize=12, textColor=HexColor("#555555"),
        alignment=TA_CENTER, spaceAfter=8,
    )
    st_bloco = ParagraphStyle(
        "BlocoCustom", parent=styles["Heading1"],
        fontName=_FONT_BOLD,
        fontSize=16, textColor=HexColor("#1e3a5f"),
        spaceBefore=18, spaceAfter=8,
    )
    st_questao = ParagraphStyle(
        "QuestaoCustom", parent=styles["Normal"],
        fontName=_FONT_NAME,
        fontSize=11, leading=15, spaceAfter=6, alignment=TA_JUSTIFY,
    )
    st_alt = ParagraphStyle(
        "AltCustom", parent=styles["Normal"],
        fontName=_FONT_NAME,
        fontSize=10.5, leading=14, leftIndent=20, spaceAfter=2,
    )
    st_gab = ParagraphStyle(
        "GabCustom", parent=styles["Normal"],
        fontName=_FONT_NAME,
        fontSize=10, leading=14, spaceAfter=4,
    )

    story = []

    # ---------------- CAPA ----------------
    story.append(Spacer(1, 3 * cm))
    story.append(Paragraph(_esc(titulo), st_titulo))
    story.append(Paragraph(
        "Preparatório para o Concurso da Guarda Municipal de Balneário Camboriú",
        st_sub,
    ))
    story.append(Spacer(1, 0.8 * cm))
    story.append(HRFlowable(
        width="60%", thickness=1, color=HexColor("#1e3a5f"),
    ))
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
        st_sub,
    ))

    total = sum(len(qs) for qs in questoes_por_bloco.values())
    story.append(Paragraph(
        f"Total: <b>{total}</b> questões em "
        f"<b>{len(questoes_por_bloco)}</b> blocos",
        st_sub,
    ))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("<b>Blocos incluídos:</b>", st_sub))
    for nome_bloco in questoes_por_bloco.keys():
        story.append(Paragraph(f"• {_esc(nome_bloco)}", st_sub))
    story.append(PageBreak())

    # ---------------- QUESTÕES ----------------
    numero = 1
    gabarito = []

    for nome_bloco, questoes in questoes_por_bloco.items():
        story.append(Paragraph(_esc(nome_bloco), st_bloco))
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=HexColor("#1e3a5f"),
        ))
        story.append(Spacer(1, 0.4 * cm))

        for q in questoes:
            story.append(Paragraph(
                f"<b>{numero}.</b> {_esc(q['enunciado'])}", st_questao,
            ))

            alts = _parse_alts(q.get("alternativas", []))
            letras = ["A", "B", "C", "D", "E"]
            for j, alt in enumerate(alts):
                letra = letras[j] if j < len(letras) else "?"
                story.append(Paragraph(
                    f"<b>{letra})</b> {_esc(alt)}", st_alt,
                ))

            story.append(Spacer(1, 0.4 * cm))
            gabarito.append({
                "numero": numero,
                "bloco": nome_bloco,
                "resposta": q.get("resposta_correta", "?"),
                "explicacao": q.get("explicacao", ""),
            })
            numero += 1

        story.append(PageBreak())

    # ---------------- GABARITO ----------------
    if incluir_gabarito and gabarito:
        story.append(Paragraph("Gabarito", st_bloco))
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=HexColor("#1e3a5f"),
        ))
        story.append(Spacer(1, 0.4 * cm))

        bloco_atual = None
        for g in gabarito:
            if g["bloco"] != bloco_atual:
                bloco_atual = g["bloco"]
                story.append(Spacer(1, 0.3 * cm))
                story.append(Paragraph(
                    f"<b>{_esc(bloco_atual)}</b>", st_gab,
                ))
            story.append(Paragraph(
                f"{g['numero']}. <b>{g['resposta']}</b>", st_gab,
            ))
            if incluir_explicacao and g["explicacao"]:
                story.append(Paragraph(
                    f"<i>{_esc(g['explicacao'])}</i>", st_gab,
                ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

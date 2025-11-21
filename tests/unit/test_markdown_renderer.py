from pathlib import Path

from it_audit_report.report.markdown_renderer import render_markdown


def test_render_markdown_renders_context(tmp_path: Path):
    template = tmp_path / "template.md.j2"
    template.write_text("Hello {{ summary.overview }}{% for risk in risks %}\\n- {{ risk.title }}{% endfor %}")

    context = {
        "summary": {"overview": "world"},
        "risks": [{"title": "Test risk"}],
        "workplan": [],
    }

    rendered = render_markdown(template, context)

    assert "Hello world" in rendered
    assert "Test risk" in rendered

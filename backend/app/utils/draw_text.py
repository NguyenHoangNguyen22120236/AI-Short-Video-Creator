def build_drawtext_filter(subtitles, font_path=None, text_effect=None):
    filters = []
    segment_base_time = subtitles[0]['start']

    for i, sub in enumerate(subtitles):
        start = sub['start'] - segment_base_time
        end = sub['end'] - segment_base_time
        text = escape_drawtext_text(sub['text'])

        fade_duration = 0.3

        # Common parts
        enable_expr = f"enable='between(t,{start},{end})'"
        base = f"text='{text}':x=(w-text_w)/2:fontcolor=white:borderw=2:bordercolor=black"
        y_default = "y=h-300"
        fontsize_default = "fontsize=55"

        if text_effect == "Fade":
            alpha_expr = (
                f"if(lt(t,{start}),0,"
                f"if(lt(t,{start + fade_duration}),(t-{start})/{fade_duration},"
                f"if(lt(t,{end - fade_duration}),1,"
                f"if(lt(t,{end}),(1-((t-{end - fade_duration})/{fade_duration})),0))))"
            )
            drawtext = f"drawtext={base}:{y_default}:{fontsize_default}:alpha='{alpha_expr}':{enable_expr}"

        elif text_effect == "Wave":
            y_expr = f"(h-300) + 10*sin(2*PI*(t-{start})*2)"
            drawtext = f"drawtext={base}:y='{y_expr}':{fontsize_default}:alpha=1:{enable_expr}"

        elif text_effect == "Slide":
            # Slide from below screen to y=h-300
            slide_y = f"(h+100)-(min(t-{start},{fade_duration})/{fade_duration})*(h - 1500)"
            drawtext = f"drawtext={base}:y='{slide_y}':{fontsize_default}:alpha=1:{enable_expr}"

        else:
            # Static
            drawtext = f"drawtext={base}:{y_default}:{fontsize_default}:alpha=1:{enable_expr}"

        if font_path:
            drawtext += f":fontfile='{font_path}'"

        filters.append(drawtext)

    return ",".join(filters)



def escape_drawtext_text(text):
    # FFmpeg drawtext expects single-quoted string. Escape single quotes correctly.
    text = text.replace("\\", "\\\\")        # Escape backslashes first
    text = text.replace(":", "\\:")          # Escape colons
    text = text.replace("'", "\\\\'")        # Escape single quotes
    text = text.replace('\n', '\\n')         # Line break in FFmpeg
    return text
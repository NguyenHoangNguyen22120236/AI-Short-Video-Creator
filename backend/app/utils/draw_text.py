def build_drawtext_filter(subtitles, font_path=None, text_effect=None):
    filters = []
    segment_base_time = subtitles[0]['start']

    for i, sub in enumerate(subtitles):
        # Normalize times
        start = sub['start'] - segment_base_time
        end = sub['end'] - segment_base_time
        text = sub['text'].replace('\n', '\\n').replace("'", "\\'").replace('"', '\\"')

        fade_duration = 0.3

        # Common parts
        enable_expr = f"enable='between(t,{start},{end})'"
        base = f"text='{text}':x=(w-text_w)/2:fontcolor=white:borderw=2:bordercolor=black"
        y_default = "y=h-100"
        fontsize_default = "fontsize=17"

        if text_effect == "Fade":
            alpha_expr = (
                f"if(lt(t,{start + 0.0}),0,"
                f"if(lt(t,{start + fade_duration}),(t-{start})/{fade_duration},"
                f"if(lt(t,{end - fade_duration}),1,"
                f"if(lt(t,{end}),(1-((t-{end - fade_duration})/{fade_duration})),0))))"
            )
            drawtext = f"drawtext={base}:{y_default}:{fontsize_default}:alpha='{alpha_expr}':{enable_expr}"

        elif text_effect == "Wave":
            # Y position oscillates with sine function
            y_expr = f"h-100 + 10*sin(2*PI*(t-{start})*2)"
            drawtext = f"drawtext={base}:y='{y_expr}':{fontsize_default}:alpha=1:{enable_expr}"

        elif text_effect == "Slide":
            # Slide up from bottom to y=h-100
            slide_y = f"(h+50)-(min(t-{start},{fade_duration})/{fade_duration})*150"
            drawtext = f"drawtext={base}:y='{slide_y}':{fontsize_default}:alpha=1:{enable_expr}"

        elif text_effect == "Scale":
            # Font size pulses up and down using sine
            font_expr = f"18 + 4*sin(2*PI*(t-{start})*1)"
            drawtext = f"drawtext={base}:{y_default}:fontsize='{font_expr}':alpha=1:{enable_expr}"

        elif text_effect == "Zoom":
            # Zoom in by scaling up font size from small to normal in fade_duration
            zoom_expr = f"if(lt(t,{start + fade_duration}), 10 + (t-{start})*((18-10)/{fade_duration}), 18)"
            drawtext = f"drawtext={base}:{y_default}:fontsize='{zoom_expr}':alpha=1:{enable_expr}"

        else:
            # Default: static subtitle
            drawtext = f"drawtext={base}:{y_default}:{fontsize_default}:alpha=1:{enable_expr}"

        if font_path:
            drawtext += f":fontfile='{font_path}'"

        filters.append(drawtext)

    return ",".join(filters)
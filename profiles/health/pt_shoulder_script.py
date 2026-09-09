from pathlib import Path

out = Path('/Users/deanradcliffe/.hermes/profiles/health/PT_Shoulder_Script.pdf')
lines = [
    ('PT APPOINTMENT SCRIPT — SHOULDER / DAILY-MOVEMENT PAIN', True),
    ('', False),
    ('“My shoulder symptoms began around April. They briefly improved, then worsened—especially in the last month. The decline happened even though I reduced upper-body weights and strengthening.', False),
    ('', False),
    ('My left shoulder is the main issue. Pain is usually triggered by small, awkward, or surprise movements rather than large muscular efforts. For example: dishes, pulling a door, pushing down to stand, backward shrug circles, elbow-out lifting, or raising my arm after dishes to check my watch. It often hurts with my elbow bent around 90 degrees and my arm at my side or slightly behind me.', False),
    ('', False),
    ('I can often tolerate pushups, planks, and moderate lifting better than those ordinary motions. I have clicking/instability sensations in both shoulders, and my right shoulder dislocated three times, last more than ten years ago. I have not had numbness, major weakness, or true giving-way.', False),
    ('', False),
    ('I suspect computer ergonomics may be contributing because my left arm does frequent window-management work. But a week away from the computer, plus ongoing ergonomic changes, has not made daily tasks like dishes reliably easier.', False),
    ('', False),
    ('Walking can also provoke the shoulder during arm swing and torso rotation. I’m somewhat guarded on walks because torsional forces through the upper body can cause pain. My plantar-fasciitis symptoms are not a major current problem.', False),
    ('', False),
    ('I’d like help assessing shoulder/scapular stability and mechanics, trunk and thoracic rotation, posture, arm swing/gait, and workstation movement habits. I want a safe plan for normal daily activity without guarding or surprise tweaks. My MRI is scheduled for September 22, pending authorization.”', False),
]

# Minimal standards-compliant one-page PDF using only Python's standard library.
def esc(s: str) -> str:
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)').replace('—', '-').replace('“', '"').replace('”', '"').replace('’', "'").replace('°', ' degrees')

def wrap(text: str, width: int = 88):
    words = text.split()
    result, current = [], ''
    for word in words:
        candidate = word if not current else current + ' ' + word
        if len(candidate) <= width:
            current = candidate
        else:
            result.append(current)
            current = word
    if current:
        result.append(current)
    return result or ['']

content_lines = []
for text, bold in lines:
    if not text:
        content_lines.append(('', False))
    else:
        content_lines.extend((part, bold) for part in wrap(text))

commands = ['BT', '/F1 11 Tf', '72 748 Td', '15 TL']
for text, bold in content_lines:
    commands.append(('/F2 11 Tf' if bold else '/F1 11 Tf'))
    commands.append(f'({esc(text)}) Tj')
    commands.append('T*')
commands.append('ET')
stream = ('\n'.join(commands) + '\n').encode('latin-1')
objects = [
    b'<< /Type /Catalog /Pages 2 0 R >>',
    b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>',
    b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'endstream',
    b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
    b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>',
]
pdf = bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
offsets = [0]
for i, obj in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf.extend(f'{i} 0 obj\n'.encode())
    pdf.extend(obj)
    pdf.extend(b'\nendobj\n')
xref = len(pdf)
pdf.extend(f'xref\n0 {len(objects)+1}\n'.encode())
pdf.extend(b'0000000000 65535 f \n')
for offset in offsets[1:]:
    pdf.extend(f'{offset:010d} 00000 n \n'.encode())
pdf.extend(f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
out.write_bytes(pdf)
print(out)
print(f'{out.stat().st_size} bytes')

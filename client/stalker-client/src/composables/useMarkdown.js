
export function useMarkdown() {
  const parseMarkdown = (markdown) => {
    if (!markdown) return ''

    let html = markdown

    html = html.replace(/^### (.*$)/gm, '<h3 class="markdown-h3">$1</h3>')
    html = html.replace(/^## (.*$)/gm, '<h2 class="markdown-h2">$1</h2>')
    html = html.replace(/^# (.*$)/gm, '<h1 class="markdown-h1">$1</h1>')

    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="markdown-strong">$1</strong>')
    html = html.replace(/\*(.*?)\*/g, '<em class="markdown-em">$1</em>')

    html = html.replace(/`([^`]+)`/g, '<code class="markdown-code">$1</code>')
    html = html.replace(/```([^`]+)```/g, '<pre class="markdown-pre"><code class="markdown-code-block">$1</code></pre>')

    const tableRegex = /(\|[^\n]+\|\n)+/g
    html = html.replace(tableRegex, (match) => {
      const rows = match.trim().split('\n')
      let tableHtml = '<table class="markdown-table">'

      rows.forEach((row, index) => {
        if (row.includes('|')) {
          const cells = row.split('|').filter(cell => cell.trim())
          if (index === 0) {
            tableHtml += '<thead><tr class="markdown-table-header">'
            cells.forEach(cell => {
              tableHtml += `<th class="markdown-th">${cell.trim()}</th>`
            })
            tableHtml += '</tr></thead><tbody>'
          } else {
            tableHtml += '<tr class="markdown-table-row">'
            cells.forEach(cell => {
              tableHtml += `<td class="markdown-td">${cell.trim()}</td>`
            })
            tableHtml += '</tr>'
          }
        }
      })

      tableHtml += '</tbody></table>'
      return tableHtml
    })

    html = html.replace(/^\s*[-*+]\s+(.+)$/gm, '<li class="markdown-li">$1</li>')
    html = html.replace(/(<li class="markdown-li">.*<\/li>)/s, '<ul class="markdown-ul">$1</ul>')

    html = html.replace(/^\s*\d+\.\s+(.+)$/gm, '<li class="markdown-li-ordered">$1</li>')
    html = html.replace(/(<li class="markdown-li-ordered">.*<\/li>)/s, '<ol class="markdown-ol">$1</ol>')

    html = html.replace(/^>\s(.+)$/gm, '<blockquote class="markdown-blockquote">$1</blockquote>')
    html = html.replace(/^---$/gm, '<hr class="markdown-hr">')
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="markdown-link" target="_blank" rel="noopener noreferrer">$1</a>')

    html = html.replace(/\n\n/g, '</p><p class="markdown-p">')
    html = html.replace(/^(?!<[h|u|o|l|t|b|p])/gm, '<p class="markdown-p">')
    html = html.replace(/(?<![>])$/gm, '</p>')

    html = html.replace(/<p class="markdown-p"><\/p>/g, '')
    html = html.replace(/<p class="markdown-p">(<[h|u|o|l|t|b])/g, '$1')
    html = html.replace(/(<\/[h|u|o|l|t|b]>)<\/p>/g, '$1')

    return html
  }

  const generateHTMLTemplate = (content) => {
    return `<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proje Analiz Dokümanı</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #007bff;
        }

        .header h1 {
            color: #007bff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header .date {
            color: #666;
            font-style: italic;
        }

        .markdown-h1 {
            color: #2c3e50;
            font-size: 2em;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }

        .markdown-h2 {
            color: #3498db;
            font-size: 1.5em;
            margin: 25px 0 15px 0;
        }

        .markdown-h3 {
            color: #27ae60;
            font-size: 1.2em;
            margin: 20px 0 10px 0;
        }

        .markdown-p {
            margin-bottom: 15px;
            text-align: justify;
        }

        .markdown-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .markdown-th {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 1px solid #2980b9;
        }

        .markdown-td {
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
            vertical-align: top;
        }

        .markdown-table-row:nth-child(even) {
            background-color: #f8f9fa;
        }

        .markdown-table-row:hover {
            background-color: #e3f2fd;
        }

        .markdown-strong {
            font-weight: 600;
            color: #2c3e50;
        }

        .markdown-em {
            font-style: italic;
            color: #7f8c8d;
        }

        .markdown-code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }

        .markdown-ul, .markdown-ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        .markdown-li {
            margin-bottom: 8px;
        }

        .markdown-blockquote {
            border-left: 4px solid #3498db;
            background: #f8f9fa;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-style: italic;
        }

        .markdown-hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, #3498db, #2ecc71);
            margin: 30px 0;
            border-radius: 1px;
        }

        .markdown-link {
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px dotted #3498db;
        }

        .markdown-link:hover {
            color: #2980b9;
            border-bottom: 1px solid #2980b9;
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }

            .container {
                box-shadow: none;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Proje Analiz Dokümanı</h1>
            <div class="date">Oluşturulma Tarihi: ${new Date().toLocaleDateString('tr-TR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })}</div>
        </div>
        ${content}
    </div>
</body>
</html>`
  }

  return {
    parseMarkdown,
    generateHTMLTemplate
  }
}

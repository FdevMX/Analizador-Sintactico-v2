"use client"

import { useState, useRef, useEffect } from 'react'
import { Moon, Sun, Github } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function Component() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [tokens, setTokens] = useState<Array<{ token: string, lexeme: string, line: number }>>([])
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const lineNumbersRef = useRef<HTMLDivElement>(null)

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light')
    document.documentElement.classList.toggle('dark')
  }

  const analyzeCode = () => {
    setOutput('Análisis completado.\n> Tokens identificados: 4\n> Errores encontrados: 0')
    setTokens([
      { token: 'KEYWORD', lexeme: 'if', line: 1 },
      { token: 'IDENTIFIER', lexeme: 'x', line: 1 },
      { token: 'OPERATOR', lexeme: '>', line: 1 },
      { token: 'NUMBER', lexeme: '0', line: 1 },
    ])
  }

  const clearAll = () => {
    setCode('')
    setOutput('')
    setTokens([])
  }

  useEffect(() => {
    const updateLineNumbers = () => {
      if (textareaRef.current && lineNumbersRef.current) {
        const lineCount = textareaRef.current.value.split('\n').length
        const lineNumbers = Array(lineCount).fill(0).map((_, i) => i + 1).join('\n')
        lineNumbersRef.current.innerText = lineNumbers
      }
    }

    updateLineNumbers()
    window.addEventListener('resize', updateLineNumbers)
    return () => window.removeEventListener('resize', updateLineNumbers)
  }, [code])

  return (
    <div className={`min-h-screen ${theme === 'dark' ? 'dark' : ''}`}>
      <div className="bg-background/80 text-foreground backdrop-blur-md backdrop-filter transition-colors duration-300">
        <header className="flex items-center justify-between p-4 border-b bg-background/90">
          <Github className="h-6 w-6" />
          <h1 className="text-2xl font-bold">Analizador</h1>
          <Button variant="ghost" onClick={toggleTheme}>
            {theme === 'light' ? <Moon className="h-6 w-6" /> : <Sun className="h-6 w-6" />}
          </Button>
        </header>
        
        <main className="container mx-auto p-4 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative font-mono text-sm">
              <div
                ref={lineNumbersRef}
                className="absolute left-0 top-0 p-2 select-none text-gray-400 dark:text-gray-600"
                style={{ width: '2em', whiteSpace: 'pre-line' }}
              ></div>
              <textarea
                ref={textareaRef}
                placeholder="Ingrese su código aquí..."
                className="w-full h-64 p-2 pl-8 bg-muted/50 backdrop-blur-sm resize-none rounded-lg"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                style={{ tabSize: 2 }}
              ></textarea>
            </div>
            <div className="font-mono text-sm">
              <div className="bg-gray-100 dark:bg-gray-800 text-green-600 dark:text-green-400 p-4 rounded-lg h-64 overflow-auto backdrop-blur-sm">
                <div className="mb-2 text-gray-500 dark:text-gray-400">$ analizador-sintactico</div>
                {output.split('\n').map((line, index) => (
                  <div key={index}>{line}</div>
                ))}
              </div>
            </div>
          </div>
          
          <div className="flex justify-center space-x-4">
            <Button onClick={analyzeCode}>Analizar</Button>
            <Button variant="outline" onClick={clearAll}>Limpiar</Button>
          </div>
          
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Token</TableHead>
                <TableHead>Lexema</TableHead>
                <TableHead>Línea</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tokens.map((token, index) => (
                <TableRow key={index}>
                  <TableCell>{token.token}</TableCell>
                  <TableCell>{token.lexeme}</TableCell>
                  <TableCell>{token.line}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </main>
      </div>
    </div>
  )
}
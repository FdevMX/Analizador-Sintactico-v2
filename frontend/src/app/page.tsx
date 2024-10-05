"use client"

import React, { useState, useRef, useEffect } from 'react';
import { Moon, Sun, Github } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

interface Token {
  token: string;
  lexeme: string;
  line: number;
  wordReserv?: boolean;
  identifier?: boolean;
  cadena?: boolean;
  numero?: boolean;
  simbolo?: boolean;
}

interface Repeticiones {
  wordReserv: number;
  identifier: number;
  cadena: number;
  numero: number;
  simbolo: number;
}

const TokenTable: React.FC<{ tokens: Token[], repeticiones: Repeticiones }> = ({ tokens, repeticiones }) => (
  <div>
    <div className="mb-4">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[200px]">Token</TableHead>
            <TableHead className="w-[200px]">Lexema</TableHead>
            <TableHead className="w-[50px]">Palabra Reservada</TableHead>
            <TableHead className="w-[50px]">Identificador</TableHead>
            <TableHead className="w-[50px]">Cadena</TableHead>
            <TableHead className="w-[50px]">Numero</TableHead>
            <TableHead className="w-[50px]">Simbolo</TableHead>
            <TableHead className="w-[50px]">Línea</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tokens.map((token, index) => (
            <TableRow key={index}>
              <TableCell className="w-[200px]">{token.token}</TableCell>
              <TableCell className="w-[200px]">{token.lexeme}</TableCell>
              <TableCell className="w-[50px]">{token.wordReserv ? 'x' : ''}</TableCell>
              <TableCell className="w-[50px]">{token.identifier ? 'x' : ''}</TableCell>
              <TableCell className="w-[50px]">{token.cadena ? 'x' : ''}</TableCell>
              <TableCell className="w-[50px]">{token.numero ? 'x' : ''}</TableCell>
              <TableCell className="w-[50px]">{token.simbolo ? 'x' : ''}</TableCell>
              <TableCell className="w-[50px]">{token.line}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>

    {/* Mini tabla para mostrar las cantidades */}
    <div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[200px]">Token</TableHead>
            <TableHead className="w-[200px]">Lexema</TableHead>
            <TableHead className="w-[50px]">Palabra Reservada</TableHead>
            <TableHead className="w-[50px]">Identificador</TableHead>
            <TableHead className="w-[50px]">Cadena</TableHead>
            <TableHead className="w-[50px]">Numero</TableHead>
            <TableHead className="w-[50px]">Simbolo</TableHead>
            <TableHead className="w-[50px]">Linea</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell className="w-[200px]">null</TableCell>
            <TableCell className="w-[200px]">null</TableCell>
            <TableCell className="w-[50px]">{repeticiones.wordReserv}</TableCell>
            <TableCell className="w-[50px]">{repeticiones.identifier}</TableCell>
            <TableCell className="w-[50px]">{repeticiones.cadena}</TableCell>
            <TableCell className="w-[50px]">{repeticiones.numero}</TableCell>
            <TableCell className="w-[50px]">{repeticiones.simbolo}</TableCell>
            <TableCell className="w-[50px]">null</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>
);

const CodeAnalyzerComponent: React.FC = () => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [tokens, setTokens] = useState<Token[]>([]);
  const [repeticiones, setRepeticiones] = useState<Repeticiones>({ wordReserv: 0, identifier: 0, cadena: 0, numero: 0, simbolo: 0 });
  const [language, setLanguage] = useState('pseudocode');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
    localStorage.setItem('theme', newTheme);
  };

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (savedTheme) {
      setTheme(savedTheme);
      document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    }

    const updateLineNumbers = () => {
      if (textareaRef.current && lineNumbersRef.current) {
        const lineCount = textareaRef.current.value.split('\n').length;
        const lineNumbers = Array(lineCount).fill(0).map((_, i) => i + 1).join('\n');
        lineNumbersRef.current.innerText = lineNumbers;
      }
    };

    updateLineNumbers();
    window.addEventListener('resize', updateLineNumbers);
    return () => window.removeEventListener('resize', updateLineNumbers);
  }, [code]);

  const contarRepeticiones = (tokens: Token[]): Repeticiones => {
    const repeticiones: Repeticiones = { wordReserv: 0, identifier: 0, cadena: 0, numero: 0, simbolo: 0 };
    tokens.forEach(token => {
      if (token.wordReserv) repeticiones.wordReserv++;
      if (token.identifier) repeticiones.identifier++;
      if (token.cadena) repeticiones.cadena++;
      if (token.numero) repeticiones.numero++;
      if (token.simbolo) repeticiones.simbolo++;
    });
    return repeticiones;
  };

  const analyzeCode = async () => {
    const codeContent = code.trim();
    if (codeContent === '') {
      setOutput('Error: Ingrese su código.');
      return;
    }
    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: codeContent, language }),
      });
      const data = await response.json();
      setTokens(data.tokens);
      setRepeticiones(contarRepeticiones(data.tokens));
      setOutput(data.errors.join('\n') || 'No se encontraron errores');
    } catch (error) {
      console.error('Error:', error);
      setOutput('Error al analizar el código');
    }
  };

  const clearAll = () => {
    setCode('');
    setOutput('');
    setTokens([]);
    setRepeticiones({ wordReserv: 0, identifier: 0, cadena: 0, numero: 0, simbolo: 0 });
  };

  return (
    <div className={`min-h-screen bg-white dark:bg-dark-gray text-black dark:text-white transition-colors duration-300`}>
      <header className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <a 
          href="https://github.com/FdevMX/Analizador-Sintactico-v2" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="text-black dark:text-white hover:bg-gray-200 dark:hover:bg-gray-800 p-3 rounded-full w-20 h-18 transition-all duration-300 flex items-center justify-center"
        >
          <Github className="h-6 w-6" />
        </a>
        <h1 className="text-2xl font-bold">Analizador</h1>
        <Button 
          variant="ghost"
          onClick={toggleTheme}
          className="text-black dark:text-white hover:bg-gray-200 dark:hover:bg-gray-800 p-3 rounded-full w-20 h-18 transition-all duration-300 flex items-center justify-center"
        >
          {theme === 'light' ? <Moon className="h-6 w-6" /> : <Sun className="h-6 w-6" />}
        </Button>
      </header>
      
      <main className="container mx-auto p-4 space-y-4">
        <div className="mb-4">
          <select
            className="p-2 bg-gray-100 dark:bg-gray-800 text-black dark:text-white rounded-lg"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            <option value="pseudocode">Pseudocódigo</option>
            <option value="java">Java (For Loop)</option>
          </select>
        </div>

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
              className="w-full h-64 p-2 pl-8 bg-gray-100 dark:bg-gray-800 text-black dark:text-white resize-none rounded-lg"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              style={{ tabSize: 2 }}
            ></textarea>
          </div>
          <div className="font-mono text-sm">
            <div className="bg-gray-100 dark:bg-gray-800 text-green-600 dark:text-green-400 p-4 rounded-lg h-64 overflow-auto">
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
        
        <TokenTable tokens={tokens} repeticiones={repeticiones} />
      </main>
    </div>
  );
};

export default CodeAnalyzerComponent;
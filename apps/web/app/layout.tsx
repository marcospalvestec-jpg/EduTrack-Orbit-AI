import type { ReactNode } from 'react';
import './globals.css';

export const metadata = { title: 'EduTrack Orbit AI', description: 'Seu espaço de estudo e foco.' };

export default function Layout({ children }: { children: ReactNode }) {
  return <html lang="pt-BR"><body>{children}</body></html>;
}

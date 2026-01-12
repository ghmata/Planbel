import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { BottomNav } from './BottomNav';

export function Layout() {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <main className="pb-20 md:pb-0 md:pl-64">
        <div className="min-h-screen">
          <Outlet />
        </div>
      </main>
      <BottomNav />
    </div>
  );
}

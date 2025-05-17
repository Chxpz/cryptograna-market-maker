import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import PortfolioMaster from './components/PortfolioMaster';
import BotsList from './components/BotsList';
import CreateBot from './components/CreateBot';
import BotDetails from './components/BotDetails';
import AdminPanel from './components/AdminPanel';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/portfolio" replace />} />
          <Route path="portfolio" element={<PortfolioMaster />} />
          <Route path="bots" element={<BotsList />} />
          <Route path="bots/:botId" element={<BotDetails />} />
          <Route path="create" element={<CreateBot />} />
          <Route path="admin" element={<AdminPanel />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;

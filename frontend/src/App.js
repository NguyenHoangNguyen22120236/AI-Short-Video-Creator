import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";

import Header from './components/Header';
import Home from './components/Home';
import HistorySeeAll from './components/HistorySeeAll';
import CreateVideo from './components/CreateVideo';
import PreviewVideo from './components/PreviewVideo';
import Authentication from './components/Authentication';
import ErrorPage from "./components/ErrorPage";

function AppContent() {
  const location = useLocation();
  const shouldShowHeader = location.pathname !== "/authentication";

  return (
    <>
      {shouldShowHeader && <Header />}

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history-see-all" element={<HistorySeeAll />} />
        <Route path="/create-video" element={<CreateVideo />} />
        <Route path="/preview-video/:id" element={<PreviewVideo />} />
        <Route path="/authentication" element={<Authentication />} />
        <Route path="/error" element={<ErrorPage />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;

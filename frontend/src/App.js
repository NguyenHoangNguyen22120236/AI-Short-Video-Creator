import React from 'react';
import {BrowserRouter, Route, Routes} from 'react-router-dom';

import Header from './components/Header';
import Home from './components/Home';
import HistorySeeAll from './components/HistorySeeAll';
import CreateVideo from './components/CreateVideo';

function App() {
  return (
    <BrowserRouter>
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/history-see-all" element={<HistorySeeAll />} />
        <Route path="/create-video" element={<CreateVideo />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

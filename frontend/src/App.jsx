import Calendar from './components/Calendar';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">IvolTutor</h1>
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            + Додати учня
          </button>
        </header>
        
        <main>
          <Calendar />
        </main>
      </div>
    </div>
  );
}

export default App;
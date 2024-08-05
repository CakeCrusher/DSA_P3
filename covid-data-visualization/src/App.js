import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import { useTransition, animated } from 'react-spring';
import './App.css';

function App() {
  const [rawData, setRawData] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/grouped_sorted_covid_merge.json');
        setRawData(response.data.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const processedData = useMemo(() => {
    return rawData.map(monthData => {
      // hash map to store peak cases by country per month
      const peakCasesByCountry = {};
      monthData.data.forEach(dayData => {
        const country = dayData.Location.Country;
        const cases = dayData.Data.Cases;
        if (!peakCasesByCountry[country] || cases > peakCasesByCountry[country].cases) {
          peakCasesByCountry[country] = { 
            cases: cases, 
            date: `${dayData.Date.Year}-${dayData.Date.Month}-${dayData.Date.Day}` 
          };
        }
      });

      const sortedPeakCases = Object.entries(peakCasesByCountry)
        .sort((a, b) => b[1].cases - a[1].cases)
        .slice(0, 10)
        .map(([country, data]) => ({ country, ...data }));

      return {
        date: monthData.date,
        data: sortedPeakCases
      };
    });
  }, [rawData]);

  const currentMonth = processedData[currentIndex];

  const handlePrevious = useCallback(() => {
    setCurrentIndex((prevIndex) => (prevIndex > 0 ? prevIndex - 1 : prevIndex));
  }, []);

  const handleNext = useCallback(() => {
    setCurrentIndex((prevIndex) => (prevIndex < processedData.length - 1 ? prevIndex + 1 : prevIndex));
  }, [processedData.length]);

  const transitions = useTransition(currentMonth?.data || [], {
    keys: item => item.country,
    from: { opacity: 0, transform: 'translate3d(100%,0,0)' },
    enter: { opacity: 1, transform: 'translate3d(0%,0,0)' },
    leave: { opacity: 0, transform: 'translate3d(-50%,0,0)' },
  });

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="App">
      <h1>Peak COVID-19 Cases by Country and Month</h1>
      <div className="navigation">
        <button onClick={handlePrevious} disabled={currentIndex === 0}>
          &larr; Previous
        </button>
        <h2>{currentMonth?.date}</h2>
        <button onClick={handleNext} disabled={currentIndex === processedData.length - 1}>
          Next &rarr;
        </button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Country</th>
            <th>Peak Cases</th>
            <th>Peak Date</th>
          </tr>
        </thead>
        <tbody>
          {transitions((style, item) => (
            <animated.tr style={style}>
              <td>{item.country}</td>
              <td>{item.cases}</td>
              <td>{item.date}</td>
            </animated.tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
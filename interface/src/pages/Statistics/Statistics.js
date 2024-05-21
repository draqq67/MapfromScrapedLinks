import React, { useState, useEffect, useRef } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './Statistics.scss';

// Register the required components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function StatisticsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const countryChartRef = useRef(null);
  const ukCountiesChartRef = useRef(null);
  const usaCountiesChartRef = useRef(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/stats')
      .then(response => response.json())
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching stats:', error);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    return () => {
      if (countryChartRef.current) {
        countryChartRef.current.destroy();
      }
      if (ukCountiesChartRef.current) {
        ukCountiesChartRef.current.destroy();
      }
      if (usaCountiesChartRef.current) {
        usaCountiesChartRef.current.destroy();
      }
    };
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!stats) {
    return <div>No data available</div>;
  }

  const countryData = {
    labels: Object.keys(stats.countries),
    datasets: [
      {
        label: 'Number of Addresses',
        data: Object.values(stats.countries),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const ukCountiesData = {
    labels: Object.keys(stats.uk_counties),
    datasets: [
      {
        label: 'Number of Addresses in UK Counties',
        data: Object.values(stats.uk_counties),
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  const usaCountiesData = {
    labels: Object.keys(stats.usa_counties),
    datasets: [
      {
        label: 'Number of Addresses in USA Counties',
        data: Object.values(stats.usa_counties),
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
        borderColor: 'rgba(255, 159, 64, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="statistics-page">
      <h1>Statistics</h1>
      <div className="stats-overview">
        <div>Addresses Not Found: {stats.address_not_found}</div>
        <div>Empty: {stats.empty}</div>
        <div>Extracted: {stats.extracted}</div>
      </div>
      <div className="charts">
        <div className="chart">
          <h2>Addresses by Country</h2>
          <Bar ref={countryChartRef} data={countryData} options={{ responsive: true, maintainAspectRatio: false }} />
        </div>
        <div className="chart">
          <h2>Addresses in UK Counties</h2>
          <Bar ref={ukCountiesChartRef} data={ukCountiesData} options={{ responsive: true, maintainAspectRatio: false }} />
        </div>
        <div className="chart">
          <h2>Addresses in USA Counties</h2>
          <Bar ref={usaCountiesChartRef} data={usaCountiesData} options={{ responsive: true, maintainAspectRatio: false }} />
        </div>
      </div>
    </div>
  );
}

export default StatisticsPage;

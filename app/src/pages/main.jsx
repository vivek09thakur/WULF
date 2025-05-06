import { useState } from "react";
import Calendar from "react-calendar";

const MainPage = () => {
  const [value, onChange] = useState(new Date());
  return (
    <>
      <div className="main">
        <div className="calendar">
          <Calendar onChange={onChange} value={value} />
        </div>
      </div>
    </>
  );
};

export default MainPage;

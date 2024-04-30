
  // Получаем элементы списка и кнопку
  const school = document.getElementById('school');
  const grupp = document.getElementById('grupp');
  const student = document.getElementById('student');

  // Заполняем список детей данными в зависимости от выбранного родителя
  const updategruppOptions = () => {
    if (school.value === '1') {
      grupp.innerHTML = '<option value="1">Ребенок 1</option><option value="2">Ребенок 2</option>';
    } else if (school.value === '2') {
      grupp.innerHTML = '<option value="3">1121Б</option><option value="4">1521Б</option>';
    } else if (school.value === '3') {
      grupp.innerHTML = '<option value="5">Ребенок 5</option><option value="6">Ребенок 6</option>';
    }
    grupp.disabled = false;
    student.disabled = true;
    student.innerHTML = '<option value="" selected>Выберите студента</option>';
  };

  // Заполняем список внуков данными в зависимости от выбранного ребенка
  const updatestudentOptions = () => {
    if (grupp.value === '1') {
      student.innerHTML = '<option value="1">Внук 1</option><option value="2">Внук 2</option>';
    } else if (grupp.value === '2') {
      student.innerHTML = '<option value="3"></option>Внук 3<option value="4">Внук 4</option>';
    } else if (grupp.value === '3') {
      student.innerHTML = '<option value="5">Сирченко михаих</option><option value="6">Малахин Антон</option>';
    } else if (grupp.value === '4') {
      student.innerHTML = '<option value="7">Федосеев Павел</option><option value="8">Внук 8</option>';
    } else if (grupp.value === '5') {
      student.innerHTML = '<option value="9">Внук 9</option><option value="10">Внук 10</option>';
    } else if (grupp.value === '6') {
      student.innerHTML = '<option value="11">Внук 11</option><option value="12">Внук 12</option>';
    }
    student.disabled = false;
  };

  // Обрабатываем событие изменения родительского списка
  school.addEventListener('change', updategruppOptions);

  // Обрабатываем событие изменения списка детей
  grupp.addEventListener('change', updatestudentOptions);


  // Получаем элементы списка и кнопку
  const parent = document.getElementById('parent');
  const child = document.getElementById('child');
  const grandchild = document.getElementById('grandchild');

  // Заполняем список детей данными в зависимости от выбранного родителя
  const updateChildOptions = () => {
    if (parent.value === '1') {
      child.innerHTML = '<option value="1">Ребенок 1</option><option value="2">Ребенок 2</option>';
    } else if (parent.value === '2') {
      child.innerHTML = '<option value="3">1121Б</option><option value="4">1521Б</option>';
    } else if (parent.value === '3') {
      child.innerHTML = '<option value="5">Ребенок 5</option><option value="6">Ребенок 6</option>';
    }
    child.disabled = false;
    grandchild.disabled = true;
    grandchild.innerHTML = '<option value="" selected>Выберите студента</option>';
  };

  // Заполняем список внуков данными в зависимости от выбранного ребенка
  const updateGrandchildOptions = () => {
    if (child.value === '1') {
      grandchild.innerHTML = '<option value="1">Внук 1</option><option value="2">Внук 2</option>';
    } else if (child.value === '2') {
      grandchild.innerHTML = '<option value="3"></option>Внук 3<option value="4">Внук 4</option>';
    } else if (child.value === '3') {
      grandchild.innerHTML = '<option value="5">Сирченко михаих</option><option value="6">Малахин Антон</option>';
    } else if (child.value === '4') {
      grandchild.innerHTML = '<option value="7">Федосеев Павел</option><option value="8">Внук 8</option>';
    } else if (child.value === '5') {
      grandchild.innerHTML = '<option value="9">Внук 9</option><option value="10">Внук 10</option>';
    } else if (child.value === '6') {
      grandchild.innerHTML = '<option value="11">Внук 11</option><option value="12">Внук 12</option>';
    }
    grandchild.disabled = false;
  };

  // Обрабатываем событие изменения родительского списка
  parent.addEventListener('change', updateChildOptions);

  // Обрабатываем событие изменения списка детей
  child.addEventListener('change', updateGrandchildOptions);

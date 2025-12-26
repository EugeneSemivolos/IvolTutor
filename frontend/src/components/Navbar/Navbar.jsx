import { useState } from 'react';
import ThemeToggle from './ThemeToggle';
import HelpPage from './HelpPage';
import styles from './Navbar.module.css';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showHelp, setShowHelp] = useState(false); // !!! 2. Стан для відображення вікна допомоги

  // Функція для відкриття допомоги та закриття меню
  const handleOpenHelp = () => {
    setShowHelp(true);
    setIsMenuOpen(false); // Закриваємо мобільне меню
  };

  return (
    <>
      <header className={styles.container}>
        {/* Ліва частина: гамбургер + назва */}
        <div className={styles.left}>
          <button
            type="button"
            className={`${styles.hamburger_menu} ${isMenuOpen ? styles.active : ''}`}
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Open menu"
            aria-expanded={isMenuOpen}
          >
            <span className={styles.hamburger_line}></span>
            <span className={styles.hamburger_line}></span>
            <span className={styles.hamburger_line}></span>
          </button>

          <h1 className={styles.title}>
            <span className={styles.title_gradient}>Tutor</span> CRM
          </h1>
        </div>

        {/* Права частина */}
        <div className={styles.right}>
          <ThemeToggle />
          <button type="button" className={styles.account_button} aria-label="Account menu">
            <span className={styles.account_initial}>A</span>
          </button>
        </div>

        {/* --- ВИПАДАЮЧЕ МЕНЮ --- */}
        <div className={`${styles.mobile_menu} ${isMenuOpen ? styles.open : ''}`}>
          <nav className={styles.mobile_menu_nav}>
            
            {/* ГРУПА 1: Основне меню */}
            <div className={styles.menu_group_top}>
              <div className={styles.menu_item}>
                <span className={styles.menu_icon}>📅</span> Календар
              </div>
              <div className={styles.menu_item}>
                <span className={styles.menu_icon}>📓</span> Журнал
              </div>
              <div className={styles.menu_item}>
                <span className={styles.menu_icon}>👥</span> Студенти
              </div>
            </div>

            {/* ГРУПА 2: Службове меню */}
            <div className={styles.menu_group_bottom}>
              <div className={styles.menu_separator}></div>
              
              <div className={styles.menu_item}>
                <span className={styles.menu_icon}>⚙️</span> Налаштування
              </div>

              <div className={styles.menu_item} onClick={handleOpenHelp}>
                <span className={styles.menu_icon}>❓</span> Допомога
              </div>
            </div>
          </nav>
        </div>
      </header>

      {showHelp && (
        <div className={styles.help_modal_overlay}>
          {/* Кнопка закриття (хрестик) */}
          <button 
            className={styles.close_help_button} 
            onClick={() => setShowHelp(false)}
          >
            ✕
          </button>
          
          {/* Сам компонент допомоги */}
          <div className={styles.help_content_wrapper}>
             <HelpPage />
          </div>
        </div>
      )}
    </>
  );
}
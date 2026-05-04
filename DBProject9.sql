-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: May 05, 2026 at 12:28 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbproject9`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `EfectueazaTransfer` (IN `p_id_sursa` INT, IN `p_id_destinatie` INT, IN `p_suma` DECIMAL(15,2), IN `p_mesaj` VARCHAR(255))   BEGIN
    START TRANSACTION;
    
    UPDATE conturi SET sold = sold - p_suma WHERE id_cont = p_id_sursa;
    
    UPDATE conturi SET sold = sold + p_suma WHERE id_cont = p_id_destinatie;
    
    INSERT INTO transferuri (id_cont_sursa, id_cont_destinatie, suma, mesaj_detaliu)
    VALUES (p_id_sursa, p_id_destinatie, p_suma, p_mesaj);
    COMMIT;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `GenereazaExtras` (IN `p_id_cont` INT)   BEGIN
    SELECT 'Transfer Trimis' AS Tip, suma, data_transfer, mesaj_detaliu 
    FROM transferuri WHERE id_cont_sursa = p_id_cont
    UNION
    SELECT 'Transfer Primit' AS Tip, suma, data_transfer, mesaj_detaliu 
    FROM transferuri WHERE id_cont_destinatie = p_id_cont;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `audit_solduri`
--

CREATE TABLE `audit_solduri` (
  `id_audit` int(11) NOT NULL,
  `id_cont` int(11) DEFAULT NULL,
  `sold_vechi` decimal(15,2) DEFAULT NULL,
  `sold_nou` decimal(15,2) DEFAULT NULL,
  `data_modificare` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `beneficiari`
--

CREATE TABLE `beneficiari` (
  `id_beneficiar` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `nume_beneficiar` varchar(100) NOT NULL,
  `iban_beneficiar` varchar(24) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clienti`
--

CREATE TABLE `clienti` (
  `id_client` int(11) NOT NULL,
  `tip_client` enum('PF','PJ') NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefon` varchar(20) DEFAULT NULL,
  `data_aderare` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clienti`
--

INSERT INTO `clienti` (`id_client`, `tip_client`, `email`, `telefon`, `data_aderare`) VALUES
(1, 'PF', 'ion@email.com', '0722111222', '2026-04-28 22:38:28'),
(2, 'PF', 'ana@email.com', '0733444555', '2026-04-28 22:38:28');

-- --------------------------------------------------------

--
-- Table structure for table `conturi`
--

CREATE TABLE `conturi` (
  `id_cont` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `id_tip_cont` int(11) NOT NULL,
  `iban` varchar(24) NOT NULL,
  `sold` decimal(15,2) DEFAULT 0.00,
  `data_deschidere` date DEFAULT curdate(),
  `status` enum('Activ','Inchis','Blocat') DEFAULT 'Activ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `conturi`
--

INSERT INTO `conturi` (`id_cont`, `id_client`, `id_tip_cont`, `iban`, `sold`, `data_deschidere`, `status`) VALUES
(1, 1, 1, 'RO12BTRL0000111122223333', 900.00, '2026-04-29', 'Activ'),
(2, 2, 1, 'RO44INGB0000555566667777', 1000.00, '2026-04-29', 'Activ');

--
-- Triggers `conturi`
--
DELIMITER $$
CREATE TRIGGER `dupa_update_sold` AFTER UPDATE ON `conturi` FOR EACH ROW BEGIN
    IF OLD.sold <> NEW.sold THEN
        INSERT INTO Audit_Solduri (id_cont, sold_vechi, sold_nou)
        VALUES (OLD.id_cont, OLD.sold, NEW.sold);
    END IF;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `verifica_sold_minim` BEFORE UPDATE ON `conturi` FOR EACH ROW BEGIN
    
    IF NEW.sold < 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Tranzactie respinsa: Fonduri insuficiente pentru sold minim!';
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `detalii_pf`
--

CREATE TABLE `detalii_pf` (
  `id_client` int(11) NOT NULL,
  `nume` varchar(50) NOT NULL,
  `prenume` varchar(50) NOT NULL,
  `cnp` char(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detalii_pf`
--

INSERT INTO `detalii_pf` (`id_client`, `nume`, `prenume`, `cnp`) VALUES
(1, 'Ionescu', 'Ion', '1234567890123'),
(2, 'Popescu', 'Ana', '2234567890123');

-- --------------------------------------------------------

--
-- Table structure for table `detalii_pj`
--

CREATE TABLE `detalii_pj` (
  `id_client` int(11) NOT NULL,
  `denumire_firma` varchar(150) NOT NULL,
  `cui` varchar(20) NOT NULL,
  `nume_administrator` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `extrasecont`
--

CREATE TABLE `extrasecont` (
  `id_extras` int(11) NOT NULL,
  `id_cont` int(11) NOT NULL,
  `perioada_start` date NOT NULL,
  `perioada_end` date NOT NULL,
  `sold_initial` decimal(15,2) NOT NULL,
  `sold_final` decimal(15,2) NOT NULL,
  `data_generare` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notificari`
--

CREATE TABLE `notificari` (
  `id_notificare` int(11) NOT NULL,
  `id_client` int(11) NOT NULL,
  `titlu` varchar(100) NOT NULL,
  `mesaj` text NOT NULL,
  `status_citit` tinyint(1) DEFAULT 0,
  `data_trimitere` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tipuricont`
--

CREATE TABLE `tipuricont` (
  `id_tip_cont` int(11) NOT NULL,
  `nume_produs` varchar(100) NOT NULL,
  `tip_client` enum('PF','PJ') NOT NULL,
  `taxa_administrare` decimal(10,2) DEFAULT 0.00,
  `moneda` char(3) NOT NULL DEFAULT 'RON',
  `descriere` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tipuricont`
--

INSERT INTO `tipuricont` (`id_tip_cont`, `nume_produs`, `tip_client`, `taxa_administrare`, `moneda`, `descriere`) VALUES
(1, 'Cont Curent', 'PF', 0.00, 'RON', 'Cont standard pentru operatiuni zilnice');

-- --------------------------------------------------------

--
-- Table structure for table `transferuri`
--

CREATE TABLE `transferuri` (
  `id_transfer` int(11) NOT NULL,
  `id_cont_sursa` int(11) NOT NULL,
  `id_cont_destinatie` int(11) NOT NULL,
  `suma` decimal(15,2) NOT NULL,
  `mesaj_detaliu` varchar(255) DEFAULT NULL,
  `data_transfer` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transferuri`
--

INSERT INTO `transferuri` (`id_transfer`, `id_cont_sursa`, `id_cont_destinatie`, `suma`, `mesaj_detaliu`, `data_transfer`) VALUES
(2, 1, 2, 100.00, 'Test transfer', '2026-04-28 22:38:47');

--
-- Triggers `transferuri`
--
DELIMITER $$
CREATE TRIGGER `trg_notificare_transfer` AFTER INSERT ON `transferuri` FOR EACH ROW BEGIN
    
    INSERT INTO notificari (id_client, titlu, mesaj)
    SELECT id_client, 'Bani primiti', CONCAT('Ai primit ', NEW.suma, ' RON. Detalii: ', NEW.mesaj_detaliu)
    FROM conturi WHERE id_cont = NEW.id_cont_destinatie;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `tranzactii`
--

CREATE TABLE `tranzactii` (
  `id_tranzactie` int(11) NOT NULL,
  `id_cont` int(11) NOT NULL,
  `tip_tranzactie` enum('Intrare','Iesire') NOT NULL,
  `suma` decimal(15,2) NOT NULL,
  `detalii` varchar(255) DEFAULT NULL,
  `data_tranzactie` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tranzactii`
--

INSERT INTO `tranzactii` (`id_tranzactie`, `id_cont`, `tip_tranzactie`, `suma`, `detalii`, `data_tranzactie`) VALUES
(1, 2, 'Intrare', 400.00, 'Depunere numerar ATM', '2026-04-28 22:40:30');

--
-- Triggers `tranzactii`
--
DELIMITER $$
CREATE TRIGGER `dupa_insert_tranzactie` AFTER INSERT ON `tranzactii` FOR EACH ROW BEGIN
    IF NEW.tip_tranzactie = 'Intrare' THEN
        UPDATE Conturi SET sold = sold + NEW.suma WHERE id_cont = NEW.id_cont;
    ELSEIF NEW.tip_tranzactie = 'Iesire' THEN
        UPDATE Conturi SET sold = sold - NEW.suma WHERE id_cont = NEW.id_cont;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_alerte_frauda`
-- (See below for the actual view)
--
CREATE TABLE `v_alerte_frauda` (
`id_transfer` int(11)
,`id_cont_sursa` int(11)
,`suma` decimal(15,2)
,`data_transfer` timestamp
,`status_risc` varchar(33)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_dashboard_conturi`
-- (See below for the actual view)
--
CREATE TABLE `v_dashboard_conturi` (
`nume_titular` varchar(150)
,`iban` varchar(24)
,`sold` decimal(15,2)
,`moneda` char(3)
,`tip_cont` varchar(100)
,`status` enum('Activ','Inchis','Blocat')
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_detalii_clienti`
-- (See below for the actual view)
--
CREATE TABLE `v_detalii_clienti` (
`id_client` int(11)
,`tip_client` enum('PF','PJ')
,`email` varchar(100)
,`nume_titular` varchar(150)
,`cod_identificare` varchar(20)
);

-- --------------------------------------------------------

--
-- Structure for view `v_alerte_frauda`
--
DROP TABLE IF EXISTS `v_alerte_frauda`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_alerte_frauda`  AS SELECT `t`.`id_transfer` AS `id_transfer`, `t`.`id_cont_sursa` AS `id_cont_sursa`, `t`.`suma` AS `suma`, `t`.`data_transfer` AS `data_transfer`, CASE WHEN `t`.`suma` > 5000 THEN 'Suma Neobisnuit de Mare' WHEN (select count(0) from `transferuri` `t2` where `t2`.`id_cont_sursa` = `t`.`id_cont_sursa` AND `t2`.`data_transfer` > `t`.`data_transfer` - interval 1 day) > 10 THEN 'Frecventa Ridicata (Posibil Atac)' ELSE 'Normal' END AS `status_risc` FROM `transferuri` AS `t` ;

-- --------------------------------------------------------

--
-- Structure for view `v_dashboard_conturi`
--
DROP TABLE IF EXISTS `v_dashboard_conturi`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_dashboard_conturi`  AS SELECT `dc`.`nume_titular` AS `nume_titular`, `co`.`iban` AS `iban`, `co`.`sold` AS `sold`, `tc`.`moneda` AS `moneda`, `tc`.`nume_produs` AS `tip_cont`, `co`.`status` AS `status` FROM ((`v_detalii_clienti` `dc` join `conturi` `co` on(`dc`.`id_client` = `co`.`id_client`)) join `tipuricont` `tc` on(`co`.`id_tip_cont` = `tc`.`id_tip_cont`)) ;

-- --------------------------------------------------------

--
-- Structure for view `v_detalii_clienti`
--
DROP TABLE IF EXISTS `v_detalii_clienti`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_detalii_clienti`  AS SELECT `c`.`id_client` AS `id_client`, `c`.`tip_client` AS `tip_client`, `c`.`email` AS `email`, CASE WHEN `c`.`tip_client` = 'PF' THEN concat(`pf`.`nume`,' ',`pf`.`prenume`) WHEN `c`.`tip_client` = 'PJ' THEN `pj`.`denumire_firma` END AS `nume_titular`, CASE WHEN `c`.`tip_client` = 'PF' THEN `pf`.`cnp` WHEN `c`.`tip_client` = 'PJ' THEN `pj`.`cui` END AS `cod_identificare` FROM ((`clienti` `c` left join `detalii_pf` `pf` on(`c`.`id_client` = `pf`.`id_client`)) left join `detalii_pj` `pj` on(`c`.`id_client` = `pj`.`id_client`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `audit_solduri`
--
ALTER TABLE `audit_solduri`
  ADD PRIMARY KEY (`id_audit`),
  ADD KEY `idx_audit_cont` (`id_cont`);

--
-- Indexes for table `beneficiari`
--
ALTER TABLE `beneficiari`
  ADD PRIMARY KEY (`id_beneficiar`),
  ADD KEY `fk_beneficiar_client` (`id_client`);

--
-- Indexes for table `clienti`
--
ALTER TABLE `clienti`
  ADD PRIMARY KEY (`id_client`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `conturi`
--
ALTER TABLE `conturi`
  ADD PRIMARY KEY (`id_cont`),
  ADD UNIQUE KEY `iban` (`iban`),
  ADD KEY `id_tip_cont` (`id_tip_cont`),
  ADD KEY `idx_client_cont` (`id_client`);

--
-- Indexes for table `detalii_pf`
--
ALTER TABLE `detalii_pf`
  ADD PRIMARY KEY (`id_client`),
  ADD UNIQUE KEY `cnp` (`cnp`);

--
-- Indexes for table `detalii_pj`
--
ALTER TABLE `detalii_pj`
  ADD PRIMARY KEY (`id_client`),
  ADD UNIQUE KEY `cui` (`cui`);

--
-- Indexes for table `extrasecont`
--
ALTER TABLE `extrasecont`
  ADD PRIMARY KEY (`id_extras`),
  ADD KEY `id_cont` (`id_cont`);

--
-- Indexes for table `notificari`
--
ALTER TABLE `notificari`
  ADD PRIMARY KEY (`id_notificare`),
  ADD KEY `id_client` (`id_client`);

--
-- Indexes for table `tipuricont`
--
ALTER TABLE `tipuricont`
  ADD PRIMARY KEY (`id_tip_cont`);

--
-- Indexes for table `transferuri`
--
ALTER TABLE `transferuri`
  ADD PRIMARY KEY (`id_transfer`),
  ADD KEY `id_cont_sursa` (`id_cont_sursa`),
  ADD KEY `id_cont_destinatie` (`id_cont_destinatie`),
  ADD KEY `idx_data_transfer` (`data_transfer`);

--
-- Indexes for table `tranzactii`
--
ALTER TABLE `tranzactii`
  ADD PRIMARY KEY (`id_tranzactie`),
  ADD KEY `id_cont` (`id_cont`),
  ADD KEY `idx_data_tranzactie` (`data_tranzactie`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_solduri`
--
ALTER TABLE `audit_solduri`
  MODIFY `id_audit` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `beneficiari`
--
ALTER TABLE `beneficiari`
  MODIFY `id_beneficiar` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `clienti`
--
ALTER TABLE `clienti`
  MODIFY `id_client` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `conturi`
--
ALTER TABLE `conturi`
  MODIFY `id_cont` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `extrasecont`
--
ALTER TABLE `extrasecont`
  MODIFY `id_extras` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notificari`
--
ALTER TABLE `notificari`
  MODIFY `id_notificare` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tipuricont`
--
ALTER TABLE `tipuricont`
  MODIFY `id_tip_cont` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transferuri`
--
ALTER TABLE `transferuri`
  MODIFY `id_transfer` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tranzactii`
--
ALTER TABLE `tranzactii`
  MODIFY `id_tranzactie` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `beneficiari`
--
ALTER TABLE `beneficiari`
  ADD CONSTRAINT `fk_beneficiar_client` FOREIGN KEY (`id_client`) REFERENCES `clienti` (`id_client`) ON DELETE CASCADE;

--
-- Constraints for table `conturi`
--
ALTER TABLE `conturi`
  ADD CONSTRAINT `conturi_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `clienti` (`id_client`),
  ADD CONSTRAINT `conturi_ibfk_2` FOREIGN KEY (`id_tip_cont`) REFERENCES `tipuricont` (`id_tip_cont`);

--
-- Constraints for table `detalii_pf`
--
ALTER TABLE `detalii_pf`
  ADD CONSTRAINT `detalii_pf_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `clienti` (`id_client`);

--
-- Constraints for table `detalii_pj`
--
ALTER TABLE `detalii_pj`
  ADD CONSTRAINT `detalii_pj_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `clienti` (`id_client`);

--
-- Constraints for table `extrasecont`
--
ALTER TABLE `extrasecont`
  ADD CONSTRAINT `extrasecont_ibfk_1` FOREIGN KEY (`id_cont`) REFERENCES `conturi` (`id_cont`);

--
-- Constraints for table `notificari`
--
ALTER TABLE `notificari`
  ADD CONSTRAINT `notificari_ibfk_1` FOREIGN KEY (`id_client`) REFERENCES `clienti` (`id_client`) ON DELETE CASCADE;

--
-- Constraints for table `transferuri`
--
ALTER TABLE `transferuri`
  ADD CONSTRAINT `transferuri_ibfk_1` FOREIGN KEY (`id_cont_sursa`) REFERENCES `conturi` (`id_cont`),
  ADD CONSTRAINT `transferuri_ibfk_2` FOREIGN KEY (`id_cont_destinatie`) REFERENCES `conturi` (`id_cont`);

--
-- Constraints for table `tranzactii`
--
ALTER TABLE `tranzactii`
  ADD CONSTRAINT `tranzactii_ibfk_1` FOREIGN KEY (`id_cont`) REFERENCES `conturi` (`id_cont`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

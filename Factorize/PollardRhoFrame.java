package Factorize;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableColumnModel;

class StepData {
    int step;
    BigInteger xi;
    BigInteger yi;
    BigInteger absDiff;
    BigInteger gcd;

    public StepData(int step, BigInteger xi, BigInteger yi, BigInteger absDiff, BigInteger gcd) {
        this.step = step;
        this.xi = xi;
        this.yi = yi;
        this.absDiff = absDiff;
        this.gcd = gcd;
    }
}

class PollardRhoAlgorithm {
    private List<StepData> steps;
    private List<BigInteger> factors;

    public PollardRhoAlgorithm() {
        steps = new ArrayList<>();
        factors = new ArrayList<>();
    }

    public List<StepData> factorizeWithSteps(BigInteger n, BigInteger x0, BigInteger y0, BigInteger c0) {
        steps.clear();
        factors.clear();
        if (n.compareTo(BigInteger.ONE) <= 0) {
            return steps;
        }
        if (n.isProbablePrime(20)) {
            factors.add(n);
            return steps;
        }

        BigInteger x = x0;
        BigInteger y = y0;
        BigInteger d = BigInteger.ONE;
        int stepCount = 0;
        BigInteger current_c = c0; 
        int maxSteps = 300;

        while (d.equals(BigInteger.ONE) && stepCount < maxSteps) {
            stepCount++;
            x = x.multiply(x).add(current_c).mod(n);
            y = y.multiply(y).add(current_c).mod(n);
            y = y.multiply(y).add(current_c).mod(n);
            BigInteger diff = x.subtract(y).abs();
            d = diff.gcd(n);
            steps.add(new StepData(stepCount, x, y, diff, d));

            if (!d.equals(BigInteger.ONE) && !d.equals(n)) {
                factors.add(d);
                BigInteger otherFactor = n.divide(d);
                if (!otherFactor.equals(BigInteger.ONE)) {
                    if (!factors.contains(otherFactor)) {
                        if (otherFactor.isProbablePrime(20)) {
                            factors.add(otherFactor);
                        } else {
                            PollardRhoAlgorithm subFactorizer = new PollardRhoAlgorithm();
                            subFactorizer.factorizeWithSteps(otherFactor, x0, y0, c0);
                            List<BigInteger> subFactors = subFactorizer.getFactors();
                            if (subFactors != null && !subFactors.isEmpty() && !subFactors.contains(otherFactor)) {
                                for (BigInteger sf : subFactors) {
                                    if (!factors.contains(sf)) {
                                        factors.add(sf);
                                    }
                                }
                            } else {
                                if (!factors.contains(otherFactor)) { 
                                    factors.add(otherFactor);
                                }
                            }
                        }
                    }
                }
                factors.sort(BigInteger::compareTo);
                return steps;
            }

            if (d.equals(n) && stepCount < maxSteps) {
                System.out.println("НОД стало равно n на шаге " + stepCount + " с c=" + current_c + ". Перезапуск.");
                steps.clear();
                x = new BigInteger("2");
                y = new BigInteger("2");
                current_c = new BigInteger("2");
                d = BigInteger.ONE;
                stepCount = 0;
            }
        }

        if (factors.isEmpty()) {
            if (!n.isProbablePrime(20)) { 
                 System.out.println("Не удалось найти делители для " + n + " в пределах лимита шагов или с опробованными константами.");
            } else if (!factors.contains(n)) { 
                factors.add(n); 
            }
        }
        factors.sort(BigInteger::compareTo); 
        return steps;
    }

    public List<BigInteger> getFactors() {
        return factors;
    }
}


public class PollardRhoFrame extends JFrame {
    private JTextField inputFieldN;
    private JTextField inputFieldX0;
    private JTextField inputFieldY0;
    private JTextField inputFieldC;
    private JButton factorButton;
    private JTable stepsTable;
    private DefaultTableModel tableModel;
    private JLabel resultLabel;
    private PollardRhoAlgorithm algorithm;

    private JLabel labelN, labelX0, labelY0, labelC;

    private static final Color YA_OAK = new Color(140, 139, 102);
    private static final Color APPLE_PIE = new Color(145, 185, 12);
    private static final Color BORDER_GREEN = new Color(0, 150, 0); 

    private static final Font CUSTOM_FONT = new Font("Chancery", Font.PLAIN, 14); 

    public PollardRhoFrame() {
        super("Факторизация Ро-методом Полларда");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(850, 650); 
        setLocationRelativeTo(null);

        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            SwingUtilities.updateComponentTreeUI(this);
        } catch (Exception e) {
            e.printStackTrace();
        }

        setLayout(new BorderLayout(15, 15));
        getContentPane().setBackground(APPLE_PIE); 
        ((JPanel) getContentPane()).setOpaque(true);
        ((JPanel) getContentPane()).setBorder(new EmptyBorder(15, 15, 15, 15));

        JPanel inputPanel = new JPanel(new GridBagLayout());
        inputPanel.setBackground(YA_OAK);
        inputPanel.setOpaque(true);
        inputPanel.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(BORDER_GREEN, 2), 
                "Параметры ввода",
                TitledBorder.CENTER,
                TitledBorder.TOP,
                CUSTOM_FONT,
                Color.BLACK 
            ),
            new EmptyBorder(10, 10, 10, 10)
        ));


        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

    
        labelN = new JLabel("Число n:");
        styleLabel(labelN);
        gbc.gridx = 0; gbc.gridy = 0; gbc.anchor = GridBagConstraints.EAST; inputPanel.add(labelN, gbc);
        inputFieldN = new JTextField("8051",15); 
        styleTextField(inputFieldN);
        gbc.gridx = 1; gbc.gridy = 0; gbc.weightx = 1.0; inputPanel.add(inputFieldN, gbc);

   
        labelX0 = new JLabel("Начальный x₀:");
        styleLabel(labelX0);
        gbc.gridx = 0; gbc.gridy = 1; gbc.anchor = GridBagConstraints.EAST; inputPanel.add(labelX0, gbc);
        inputFieldX0 = new JTextField("2", 15);
        styleTextField(inputFieldX0);
        gbc.gridx = 1; gbc.gridy = 1; gbc.weightx = 1.0; inputPanel.add(inputFieldX0, gbc);

        labelY0 = new JLabel("Начальный y₀:");
        styleLabel(labelY0);
        gbc.gridx = 0; gbc.gridy = 2; gbc.anchor = GridBagConstraints.EAST; inputPanel.add(labelY0, gbc);
        inputFieldY0 = new JTextField("2", 15);
        styleTextField(inputFieldY0);
        gbc.gridx = 1; gbc.gridy = 2; gbc.weightx = 1.0; inputPanel.add(inputFieldY0, gbc);

        labelC = new JLabel("Константа c (в x²+c):");
        styleLabel(labelC);
        gbc.gridx = 0; gbc.gridy = 3; gbc.anchor = GridBagConstraints.EAST; inputPanel.add(labelC, gbc);
        inputFieldC = new JTextField("1", 15);
        styleTextField(inputFieldC);
        gbc.gridx = 1; gbc.gridy = 3; gbc.weightx = 1.0; inputPanel.add(inputFieldC, gbc);
        
        factorButton = new JButton("Факторизовать");
        factorButton.setBackground(YA_OAK);
        factorButton.setForeground(APPLE_PIE);
        factorButton.setFont(CUSTOM_FONT);
        factorButton.setOpaque(true);
        factorButton.setBorderPainted(false);
        factorButton.setFocusPainted(false);
        gbc.gridx = 0; gbc.gridy = 4; gbc.gridwidth = 2; gbc.anchor = GridBagConstraints.CENTER; gbc.fill = GridBagConstraints.NONE; inputPanel.add(factorButton, gbc);

        resultLabel = new JLabel("Факторы: ");
        resultLabel.setFont(CUSTOM_FONT);
        resultLabel.setForeground(YA_OAK); 
        resultLabel.setHorizontalAlignment(SwingConstants.CENTER);
        resultLabel.setBorder(new EmptyBorder(10,0,0,0));

        String[] columnNames = {"i", "x_i", "y_i", "|x_i - y_i|", "НОД(|x_i - y_i|, n)"};
        tableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        stepsTable = new JTable(tableModel);
        stepsTable.setFillsViewportHeight(true);
        stepsTable.setRowHeight(20);
        stepsTable.setBackground(YA_OAK);
        stepsTable.setForeground(APPLE_PIE);
        stepsTable.setShowGrid(true);
        stepsTable.setGridColor(BORDER_GREEN);
        stepsTable.setFont(new Font("Consolas", Font.BOLD, 15));
        stepsTable.getTableHeader().setBackground(YA_OAK);
        stepsTable.getTableHeader().setForeground(APPLE_PIE);
        stepsTable.getTableHeader().setFont(new Font("Consolas", Font.BOLD, 15));

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(JLabel.CENTER);
        TableColumnModel columnModel = stepsTable.getColumnModel();
        for (int i = 0; i < columnNames.length; i++) {
            columnModel.getColumn(i).setCellRenderer(centerRenderer);
        }

        JScrollPane tableScrollPane = new JScrollPane(stepsTable);
        tableScrollPane.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(BORDER_GREEN), 
                "Шаги факторизации",
                TitledBorder.LEFT,
                TitledBorder.TOP,
                CUSTOM_FONT,
                Color.BLACK 
            ),
            new EmptyBorder(5, 5, 5, 5)
        ));
        tableScrollPane.setBackground(YA_OAK); 
        tableScrollPane.getViewport().setBackground(YA_OAK); 

        algorithm = new PollardRhoAlgorithm();

        factorButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                factorizeNumber();
            }
        });

        add(inputPanel, BorderLayout.NORTH);
        add(tableScrollPane, BorderLayout.CENTER);
        add(resultLabel, BorderLayout.SOUTH);
        
        setVisible(true);
    }

    private void styleTextField(JTextField textField) {
        textField.setBackground(YA_OAK);
        textField.setForeground(APPLE_PIE);
        textField.setFont(CUSTOM_FONT);
        textField.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(BORDER_GREEN, 1),
            new EmptyBorder(2, 5, 2, 5) 
        ));
    }

    private void styleLabel(JLabel label) {
        label.setFont(CUSTOM_FONT);
        label.setForeground(APPLE_PIE); 
    }
    
    private BigInteger parseBigIntegerInput(JTextField field, String fieldName, String defaultValue) {
        String text = field.getText().trim();
        if (text.isEmpty()) {
            field.setText(defaultValue); 
            return new BigInteger(defaultValue);
        }
        try {
            return new BigInteger(text);
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Некорректный ввод для '" + fieldName + "'. Введите целое число. Используется значение по умолчанию: " + defaultValue, "Ошибка ввода", JOptionPane.ERROR_MESSAGE);
            field.setText(defaultValue); 
            return new BigInteger(defaultValue);
        }
    }

    private void factorizeNumber() {
        tableModel.setRowCount(0);
        resultLabel.setText("Факторы: ");

        BigInteger numberToFactor;
        BigInteger x0;
        BigInteger y0;
        BigInteger c;

        String inputTextN = inputFieldN.getText().trim();
        if (inputTextN.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Пожалуйста, введите число n.", "Ошибка ввода", JOptionPane.WARNING_MESSAGE);
            return;
        }
        try {
            numberToFactor = new BigInteger(inputTextN);
            if (numberToFactor.compareTo(BigInteger.ONE) <= 0) {
                JOptionPane.showMessageDialog(this, "Число n должно быть больше 1.", "Ошибка ввода", JOptionPane.WARNING_MESSAGE);
                return;
            }
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Некорректный ввод для n. Введите целое число.", "Ошибка ввода", JOptionPane.ERROR_MESSAGE);
            return;
        }
        x0 = parseBigIntegerInput(inputFieldX0, "x₀", "2");
        y0 = parseBigIntegerInput(inputFieldY0, "y₀", "2");
        c  = parseBigIntegerInput(inputFieldC,  "c",  "1");


        try {
            List<StepData> steps = algorithm.factorizeWithSteps(numberToFactor, x0, y0, c);
            List<BigInteger> factors = algorithm.getFactors();

            if (steps != null) {
                for (StepData step : steps) {
                    tableModel.addRow(new Object[]{
                        step.step,
                        step.xi,
                        step.yi,
                        step.absDiff,
                        step.gcd
                    });
                }
            }

            if (factors != null && !factors.isEmpty()) {
                if (factors.size() == 1 && factors.get(0).equals(numberToFactor) && !numberToFactor.isProbablePrime(20) && numberToFactor.bitLength() > 10 ) { 
                     if (steps.isEmpty() && !numberToFactor.isProbablePrime(20)) { 
                        resultLabel.setText("Факторы: " + numberToFactor + " (вероятно, простое)");
                     } else if (steps.size() >= 299990) { 
                        resultLabel.setText("Факторы: Не найдены (достигнут лимит итераций). " + numberToFactor + " может быть простым или требовать других параметров.");
                     }
                     else {
                        resultLabel.setText("Факторы: " + numberToFactor + " (возможно, простое или требуются другие параметры/больше итераций)");
                     }
                } else {
                    StringBuilder factorsText = new StringBuilder("Факторы: ");
                    for (int i = 0; i < factors.size(); i++) {
                        factorsText.append(factors.get(i));
                        if (i < factors.size() - 1) {
                            factorsText.append(" * ");
                        }
                    }
                    resultLabel.setText(factorsText.toString());
                }
            } else {
                 resultLabel.setText("Факторы: Не найдены (число " + numberToFactor + " может быть простым, или требуются другие параметры/больше итераций)");
            }
            resultLabel.setForeground(YA_OAK); 
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this, "Произошла ошибка во время факторизации: " + ex.getMessage(), "Ошибка", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(PollardRhoFrame::new);
    }
}
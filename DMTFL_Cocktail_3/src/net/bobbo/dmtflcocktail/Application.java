package net.bobbo.dmtflcocktail;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Application {
  private JButton testButton;
  private JPanel panelMain;

  public Application() {
    testButton.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
        System.out.println("TEST!");
      }
    });
  }



  public static void main(String[] args) {
    JFrame frame = new JFrame("DMTFL Cocktail 3");
    frame.setContentPane(new Application().panelMain);
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.pack();
    frame.setVisible(true);
  }
}

# Librería para calcular transferencia de calor lineal en paredes compuestas dispuestas en serie
# solo incluye mecanismos de conducción y convección

import numpy as np
import matplotlib.pyplot as plt

class ParedCompuesta:
    def resistencia_conveccion(self, alfa, A):
        """Calcula la resistencia a transferencia de calor por convección

        Parámetros
        ----------
        alfa : float
            Coeficiente de transferencia de calor por convección [W/m^2°C]
        A : float
            Área de transferencia de calor [m^2]

        Retorna
        -------
        R : float
            Resistencia a transferencia de calor por convección [°C/W]
        """
        R = 1/(alfa*A)
        return R

    #calcular resistencia a conveccion interna con coeficiente de transferencia de calor

    def resistencia_conduccion(self, L, k, A):
        """Calcula la resistencia a transferencia de calor por conducción

        Parámetros
        ----------
        L : float
            Longitud de transferencia de calor [m]
        k : float
            Conductividad térmica [W/m°C]
        A : float
            Área de transferencia de calor [m^2]

        Retorna
        -------
        R : float
            Resistencia a transferencia de calor por conducción [°C/W]
        """
        R = L/(k*A)
        return R

    def resistencia_total(self, R):
        """Calcula la resistencia total a transferencia de calor

        Parámetros
        ----------
        R : list
            Lista de resistencias a transferencia de calor [°C/W]

        Retorna
        -------
        R_tot : float
            Resistencia total a transferencia de calor [°C/W]
        """
        np_R = np.array(R)
        R_tot = np.sum(np_R)
        return R_tot

    def flujo_calor(self, R_tot, T1, T2):
        """Calcula el flujo de calor

        Parámetros
        ----------
        R_tot : float
            Resistencia total a transferencia de calor [°C/W]
        T1 : float
            Temperatura 1 [°C]
        T2 : float
            Temperatura 2 [°C]

        Retorna
        -------
        Q : float
            Flujo de calor [W]
        """
        Q = (T1-T2)/R_tot
        return Q

    def temperatura(self, R_tot, Q, T1):
        """Calcula la temperatura

        Parámetros
        ----------
        R_tot : float
            Resistencia total a transferencia de calor [°C/W]
        Q : float
            Flujo de calor [W]
        T1 : float
            Temperatura 1 [°C]

        Retorna
        -------
        T2 : float
            Temperatura 2 [°C]
        """
        T2 = T1 - Q*R_tot
        return T2

    def coeficiente_conductividad(self, A, L, T1, T2, Q):
        """Calcula el coeficiente de conductividad

        Parámetros
        ----------
        A : float
            Área de transferencia de calor [m^2]
        L : float
            Longitud de transferencia de calor [m]
        T1 : float
            Temperatura 1 [°C]
        T2 : float
            Temperatura 2 [°C]
        Q : float
            Flujo de calor [W]

        Retorna
        -------
        k : float
            Coeficiente de conductividad [W/m°]
        """
        k = Q*L/(A*(T1-T2))
        return k

    def coeficiente_conveccion(self, A, T1, T2, Q):
        """Calcula el coeficiente de convección

        Parámetros
        ----------
        A : float
            Área de transferencia de calor [m^2]
        T1 : float
            Temperatura 1 [°C]
        T2 : float
            Temperatura 2 [°C]
        Q : float
            Flujo de calor [W]

        Retorna
        -------
        alfa : float
            Coeficiente de convección [W/m^2°C]
        """
        alfa = Q/(A*(T1-T2))
        return alfa

    def calcular_pared_compuesta(self, condiciones_interior, capas, condiciones_exterior, area):
        """Calcula la transferencia de calor en una pared compuesta

        Parámetros
        ----------
        condiciones_interior : list
            Condiciones interiores {T: temperatura [°C], h: coeficiente de convección [W/m^2°C]}
        capas : list
            Lista de capas de la pared compuesta {L: longitud [m], k: conductividad [W/m°C]}
        condiciones_exterior : list
            Condiciones exteriores {T: temperatura [°C], h: coeficiente de convección [W/m^2°C]}
        area : float
            Área de transferencia de calor [m^2]

        Retorna
        -------
        {
            Q: flujo de calor [W],
            T_interior: temperatura interior [°C],
            T_paredes: lista de temperaturas de las paredes [°C],
            T_exterior: temperatura exterior [°C],
            R_tot: resistencia total [°C/W],
            R_conveccion_interna: resistencia a convección interna [°C/W],
            R_capas: lista de resistencias a conducción [°C/W]
            R_conveccion_externa: resistencia a convección externa [°C/W],
            fig: gráfico de temperaturas a lo largo de la pared compuesta
        }
        """
        R_conveccion_interna = self.resistencia_conveccion(condiciones_interior['h'], area)
        R_conveccion_externa = self.resistencia_conveccion(condiciones_exterior['h'], area)
        R_tot = 0
        R_tot += R_conveccion_interna
        R_capas = []
        for capa in capas:
            R_capas.append(self.resistencia_conduccion(capa['L'], capa['k'], area))
        R_tot += self.resistencia_total(R_capas)
        R_tot += R_conveccion_externa
        Q = self.flujo_calor(R_tot, condiciones_interior['T'], condiciones_exterior['T'])

        T_pared_interna = self.temperatura(R_conveccion_interna, Q, condiciones_interior['T'])
        temperaturas = [T_pared_interna]
        for i in range(len(R_capas)):
            temperaturas.append(self.temperatura(R_capas[i], Q, temperaturas[i]))
        fig, ax = self.plot_pared_compuesta(condiciones_interior['T'], temperaturas, condiciones_exterior['T'], capas)

        return {
            'Q': Q,
            'T_interior': condiciones_interior['T'],
            'T_paredes': temperaturas,
            'T_exterior': condiciones_exterior['T'],
            'R_tot': R_tot,
            'R_conveccion_interna': R_conveccion_interna,
            'R_capas': R_capas,
            'R_conveccion_externa': R_conveccion_externa,
            'fig': fig,
        }

    def plot_pared_compuesta(self, T_interior, T_paredes, T_exterior, capas):
        """Grafica la transferencia de calor en una pared compuesta

        Parámetros
        ----------
        T_interior : float
            Temperatura interior [°C]
        T_paredes : list
            Lista de temperaturas de las paredes [°C]
        T_exterior : float
            Temperatura exterior [°C]
        capas : list
            Lista de capas de la pared compuesta

        Retorna
        -------
        fig : matplotlib.figure.Figure
            Figura de matplotlib
        ax : matplotlib.axes._subplots.AxesSubplot
            Ejes de matplotlib
        """

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(T_paredes, label='Temperatura')
        ax.plot([0, len(T_paredes)-1], [T_interior, T_exterior], label='Condiciones')
        # plot capas
        for i in range(len(capas)):
            nombre = capas[i]['nombre'] if 'nombre' in capas[i] else 'Capa {}'.format(i+1)
            ax.plot([i, i+1], [T_paredes[i], T_paredes[i+1]], label=nombre)
        ax.set_xlabel('Capas')
        ax.set_ylabel('Temperatura [°C]')
        ax.set_title('Transferencia de calor en pared compuesta')

        ax.legend()
        return fig, ax
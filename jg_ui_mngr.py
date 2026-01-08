# ----------------------------------------------------------------------------------
#
# (c) 2025 J&G Aeroembed.
#
# Filename: jg_ui_mngr.py
#
# Description: JG X-Pi UI Mngr
#
# ----------------------------------------------------------------------------------

# IMPORTS --------------------------------------------------------------------------
import logging
import traceback
import tkinter

from tkinter import ttk
from PIL import Image, ImageTk


from jg_xpi_controls_sw.jg_xpi_controls_mngr.jg_xpi_mngr_events import JgXPiMngrEvents
from jg_xpi_controls_sw.jg_ui_mngr.jg_ui_widgets.toggle_switch import ToggleSwitch
from jg_xpi_controls_sw.jg_ui_mngr.jg_ui_widgets.circular_toggle_button import CircularToggleButton
from jg_xpi_controls_sw.jg_ui_mngr.jg_ui_widgets.jg_three_state_switch import ThreeStateSwitch
from jg_xpi_controls_sw.jg_ui_mngr.jg_ui_widgets.jg_scroll_snap import SnapScrollController
from jg_xpi_controls_sw.jg_ui_mngr.jg_ui_widgets.jg_momentary_state_switch import MomentaryThreeStateSwitch
# ----------------------------------------------------------------------------------

# LOGGING --------------------------------------------------------------------------
log = logging.getLogger("JgUiMngr")
# ----------------------------------------------------------------------------------

# FUNCTIONS ------------------------------------------------------------------------
class JGUiMngr:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.jg_ui_mngr_events_cb = None

        self.tk.configure(bg="black")

        # Initial Screen size
        self.WINDOW_WIDTH = self.tk.winfo_screenwidth()
        self.WINDOW_HEIGHT = self.tk.winfo_screenheight()
        self.tk.overrideredirect(True)

        style = ttk.Style()
        style.configure("Red.TButton", foreground="white", background="red", padding=(2, 10))

        return

    def start(self) -> bool:
        log.debug("Enter")
        done = False

        try:
            # Setup the GUI
            self.tk.title("J&G Aeroembed X-Pi Controls")
            self.tk.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+0+0")
            self.tk.columnconfigure(0, weight=1)

            # Stop button
            
            self._stop_btn = ttk.Button(self.tk,
                                    text="X",
                                    style="Red.TButton",
                                    command=self._stop_btn_press)
            self._stop_btn.place(x=1830, y=0)
            self._stop_btn.configure(state="enabled")

            # Up Pedestal Frame
            up_line_pedestal = tkinter.Frame(self.tk, bg="black")
            up_line_pedestal.place(x=250, y=5)

            # Trim Selector Frame
            trim_selector_frame = tkinter.Frame(up_line_pedestal, bg="black")
            trim_selector_frame.pack(side=tkinter.LEFT, padx=3)

            # Trim Selector Labels
            tkinter.Label(trim_selector_frame,  text="TRIM\nSELECT\nOFF",  font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack()


            # Button Frame
            button_selector_frame = tkinter.Frame(trim_selector_frame, bg="black")
            button_selector_frame.pack()

            # Trim Selector switch
            tkinter.Label(button_selector_frame, text="P\nI\nL\nO\nT", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT)
            trim_selector = ToggleSwitch(button_selector_frame,
                                        image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/trim_selector_copilot.png", 
                                        image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/trim_selector_pilot.png", 
                                        orientation="horizontal", 
                                        command=lambda: self._trim_selector_button_toggle(trim_selector.is_on))
            trim_selector.pack(side=tkinter.LEFT, padx=20)
            tkinter.Label(button_selector_frame, text="C\nO\nP\nI\nL\nO\nT", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT)
           
            # Engine Stop and Feather Buttons Full Frame
            feather_button_main_frame = tkinter.Frame(up_line_pedestal, bg="black")
            feather_button_main_frame.pack(side=tkinter.LEFT, padx=30)

           # Engine Stop and Feather left
            feather_button_left = ToggleSwitch(feather_button_main_frame,
            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/stop_feather_open.png", 
            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/stop_feather_closed.png",
            command=lambda: self._engine_stop_feather_pressed([0, feather_button_left.is_on]))
            feather_button_left.pack(side=tkinter.LEFT, padx=3)

            tkinter.Label(feather_button_main_frame, text="ENGINE STOP AND\nFEATHER\n\nPULL", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT)

           # Engine Stop and Feather right
            feather_button_right = ToggleSwitch(feather_button_main_frame,
            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/stop_feather_open.png", 
            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/stop_feather_closed.png",
            command=lambda: self._engine_stop_feather_pressed([1, feather_button_right.is_on]))
            feather_button_right.pack(side=tkinter.LEFT, padx=3, pady=10)

            # Aeroembed Logo
            jg_aeroembed_logo = Image.open("jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/jg_aeroembed_logo.png")
            jg_aeroembed_logo_resized = jg_aeroembed_logo.resize((399, 137), Image.LANCZOS)
            self.tk_jg_aeroembed_logo = ImageTk.PhotoImage(jg_aeroembed_logo_resized)
            jg_aeroembed_logo_label = tkinter.Label(up_line_pedestal, image=self.tk_jg_aeroembed_logo, bg="black")
            jg_aeroembed_logo_label.pack(side=tkinter.LEFT, padx=10)



           
            # Main Flap frame
            flap_controller_frame = tkinter.Frame(self.tk, width=280, height=700, bg="black")
            flap_controller_frame.place(x=1640, y=75)
            flap_controller_frame.pack_propagate(False)

            # verticcal label "FLAPS"
            flaps_label = tkinter.Label(flap_controller_frame, text="F\nL\nA\nP\nS", font=("DIN Bold", 24, "bold"), fg="#C8C2A8", bg="black")
            flaps_label.place(x=0, y=165)

            # 1/4 and 1/2 slider labels both sides
            tkinter.Label(flap_controller_frame, text="1/4", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=36, y=220)
            tkinter.Label(flap_controller_frame, text="1/4", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=225, y=220)  
            tkinter.Label(flap_controller_frame, text="1/2", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=36, y=290)  
            tkinter.Label(flap_controller_frame, text="1/2", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=225, y=290)


            # creating the slider
            flaps_scroll = SnapScrollController(flap_controller_frame, 
                                                x_position=74, 
                                                y_position=40, 
                                                w_length=400, 
                                                w_width=200, 
                                                image_paths=["jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/flaps_up.png", 
                                                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/flaps_quarter.png", 
                                                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/flaps_half.png",
                                                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/flaps_down.png"],
                                                command=lambda: self.__flap_lever_moved(flaps_scroll.last_position))

            # Labels UP y DN
            tkinter.Label(flap_controller_frame, text="UP", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=125, y=0)
            tkinter.Label(flap_controller_frame, text="DN", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=125, y=550)


            # Parking Break button
            tkinter.Label(text="PARKING\nBRAKE", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=85, y=440)
            parking_break = CircularToggleButton(
            self.tk, 
            x=60, 
            y=490, 
            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/brake_pressed.png", 
            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/brake_released.png", 
            command=self._parking_break_btn_press)          

            # Main Landing Gear switch Frame
            main_lg_frame = tkinter.Frame(self.tk, bg="black")
            main_lg_frame.place(x=55, y=120)


            # Left label
            lg_left_label = tkinter.Frame(main_lg_frame, bg="black")
            lg_left_label.pack(side=tkinter.LEFT)
            tkinter.Label(lg_left_label, text="L\nA\nN\nD\nI\nN\nG\n\nG\nE\nA\nR", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack()

            # Landing Gear Switch
            tkinter.Label(main_lg_frame, text="UP", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.TOP)
            lg_switch = ToggleSwitch(main_lg_frame,
            is_on = True,
            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/landing_gear_up.png", 
            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/landing_gear_down.png",
            command=lambda: self._lg_switch_toggle(lg_switch.is_on))
            lg_switch.pack(side=tkinter.TOP, padx=25)
            tkinter.Label(main_lg_frame, text="DOWN", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.TOP)


            # Medium Pedestal Frame
            medium_line_pedestal = tkinter.Frame(self.tk, bg="black")
            medium_line_pedestal.place(x=400, y=350)

        
            # ---Fuel--- Section Frame
            fuel_section_frame = tkinter.Frame(medium_line_pedestal, bg="black")
            fuel_section_frame.pack(side=tkinter.LEFT, padx=5)

            # Fuel Label
            tkinter.Label(fuel_section_frame, 
            text="|" + "-"*30 + "FUEL" + "-"*30 + "|", 
            font=("DIN Bold", 16, "bold"), 
            fg="#C8C2A8", 
            bg="black").pack()

            # Left boost fuel switch
            left_boost_fuel_switch = ThreeStateSwitch(
                fuel_section_frame,
                width=60,
                height=180,
                image_paths=("jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_up.png", 
                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_off.png", 
                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_down.png"),
                command=lambda: self._fuel_pump_switch_pressed(left_boost_fuel_switch.state, "left"))
            left_boost_fuel_switch.pack(side=tkinter.LEFT, padx=10)

            # Main fuel control frame
            main_fuel_frame = tkinter.Frame(fuel_section_frame, bg="black")
            main_fuel_frame.pack(side=tkinter.LEFT, padx=10)

            # Fuel Control Top Labels
            fuel_top_labels = tkinter.Frame(main_fuel_frame, bg="black")
            fuel_top_labels.pack()
            tkinter.Label(fuel_top_labels, text="L\nSHUT OFF\nOPEN", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT, padx=20)
            tkinter.Label(fuel_top_labels, text="R\nSHUT OFF\nOPEN", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT, padx=20)

            # Fuel Shutoff Switches
            fuel_shutoff_frame = tkinter.Frame(main_fuel_frame, bg="black")
            fuel_shutoff_frame.pack()
            fuel_shutoff_left = ToggleSwitch(fuel_shutoff_frame, 
                                            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_up.png", 
                                            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_down.png",
                                            command=lambda: self._fuel_shut_off_button_pressed(fuel_shutoff_left.is_on, "left"))
            fuel_shutoff_left.pack(side=tkinter.LEFT, padx=45)
            fuel_shutoff_right = ToggleSwitch(fuel_shutoff_frame,
                                             image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_up.png", 
                                             image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_down.png",
                                             command=lambda: self._fuel_shut_off_button_pressed(fuel_shutoff_right.is_on,"right"))
            fuel_shutoff_right.pack(side=tkinter.LEFT, padx=45)

            # Fuel Bottom Label
            tkinter.Label(main_fuel_frame, text="CLOSED", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(pady=10)

            # Right boost fuel switch
            right_boost_fuel_switch = ThreeStateSwitch(
                fuel_section_frame,
                width=60,
                height=180,
                image_paths=("jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_up.png", 
                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_off.png", 
                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_down.png"),
                command=lambda: self._fuel_pump_switch_pressed(right_boost_fuel_switch.state, "right")
            )
            right_boost_fuel_switch.pack(side=tkinter.LEFT, padx=10)

            # Main hydraulic switch Frame
            main_hydr_Switch_frame = tkinter.Frame(medium_line_pedestal, bg="black")
            main_hydr_Switch_frame.pack(side=tkinter.LEFT, padx=0)

            # Hydraulic Top Labels
            top_labels = tkinter.Frame(main_hydr_Switch_frame, bg="black")
            top_labels.pack()
            tkinter.Label(top_labels, text="L", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT, padx=20)
            center_label = tkinter.Label(top_labels, text="HYDR\n SHUT OFF\n OPEN", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black")
            center_label.pack(side=tkinter.LEFT, padx=20)
            tkinter.Label(top_labels, text="R", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").pack(side=tkinter.LEFT, padx=20)

            # Hydraulic Shutoff Switches
            hydr_shutoff_frame = tkinter.Frame(main_hydr_Switch_frame, bg="black")
            hydr_shutoff_frame.pack()
            hydr_shutoff_left = ToggleSwitch(hydr_shutoff_frame, 
                                            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_up.png", 
                                            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_down.png",
                                            command=lambda: self._hydr_shut_off_button_pressed(hydr_shutoff_left.is_on, "left"))
            hydr_shutoff_left.pack(side=tkinter.LEFT, padx=75)
            hydr_shutoff_right = ToggleSwitch(hydr_shutoff_frame, 
                                            image_off_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_up.png", 
                                            image_on_path="jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/switch_down.png", 
                                            command=lambda: self._hydr_shut_off_button_pressed(hydr_shutoff_right.is_on,"right"))
            hydr_shutoff_right.pack(side=tkinter.LEFT, padx=75)

            # Hydraulic Bottom Label
            tkinter.Label(main_hydr_Switch_frame, text="CLOSED", font=("Arial", 16, "bold"), bg="black").pack(pady=10)

            # Trim Aux Frame
            trim_aux_frame = tkinter.Frame(self.tk, bg="black", width=170, height=300)
            trim_aux_frame.place(x=1475, y=440)

            tkinter.Label(trim_aux_frame, text="A\nU\nX\nT\nR\nI\nM", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=0, y=40)

            tkinter.Label(trim_aux_frame, text="DOWN", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=55, y=0)

            aux_trim_switch = MomentaryThreeStateSwitch(
                trim_aux_frame, 
                width=60, 
                height=170,
                image_paths=("jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_up.png", 
                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_off.png", 
                "jg_xpi_controls_sw/jg_ui_mngr/jg_ui_widgets/img/button_down.png"), 
                on_up=lambda: self._aux_trim_button_pressed(aux_trim_switch.state),
                on_center=lambda: self._aux_trim_button_pressed(aux_trim_switch.state),
                on_down=lambda: self._aux_trim_button_pressed(aux_trim_switch.state)
                )
            aux_trim_switch.place(x=35, y=30)

            tkinter.Label(trim_aux_frame, text="UP", font=("DIN Bold", 16, "bold"), fg="#C8C2A8", bg="black").place(x=80, y=240)


            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.format_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.format_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
    
    def _stop_btn_press(self) -> bool:
        log.debug("Enter")
        done = False

        try:
            log.debug("Requesting XPi Controls Manaer stop")
            self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_STOP, None)
            self.tk.destroy()
            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.fornat_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.fornat_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)

    def _parking_break_btn_press(self) -> bool:
        log.debug("Enter")
        done = False

        try:
            log.debug("Requesting XPi Controls Manager Toggle Parking Break")
            self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_HYDR_PARKING_BREAK, None)
            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.format_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.format_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)

    def _hydr_shut_off_button_pressed(self, button_state, button) -> bool:
        log.debug("Enter")
        done = False

        try:
            if button == "left" and  button_state == True:
                log.debug("Requesting XPi Controls Manager Close Left Hydraulic Fluid Cutoff Switch")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_HYDR_SHUT_OFF_L, 6)
            elif  button == "left" and  button_state == False:
                log.debug("Requesting XPi Controls Manager Open Left Hydraulic Fluid Cutoff Switch")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_HYDR_SHUT_OFF_L, 0)
            elif button == "right" and  button_state == True: 
                log.debug("Requesting XPi Controls Manager Close Right Hydraulic Fluid Cutoff Switch")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_HYDR_SHUT_OFF_R, 6)
            else:
                log.debug("Requesting XPi Controls Manager Close Right Hydraulic Fluid Cutoff Switch")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_HYDR_SHUT_OFF_R, 0)
            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.format_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.format_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
    
    def _lg_switch_toggle(self, button_state) -> bool:
        log.debug("Enter")
        done = False

        try:
            log.debug("Toggling landing gear switch")
            self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_CTRL_LG, button_state)
            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.fornat_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.fornat_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
    
    def _fuel_shut_off_button_pressed(self, button_state, button) -> bool:
        log.debug("Enter")
        done = False

        try:
            if button == "left":
                log.debug("Requesting XPi Controls Manager Toggle Left Fuel valve Switch")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_VALVE_L, button_state)
            elif button == "right": 
                log.debug("Requesting XPi Controls Manager Toggle Right Fuel Valve Switch")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_VALVE_R, button_state)
            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.fornat_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.fornat_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
    
    def _fuel_pump_switch_pressed(self, button_state, button) -> bool:
        log.debug("Enter")
        done = False

        try:
            if button == "left" and  button_state == 0:
                log.debug("Requesting XPi Controls Manager Use main Left Pump")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_PUMP_BOOST_L, 1)
            elif  button == "left" and  button_state == 1:
                log.debug("Requesting XPi Controls Manager Don't use any Left Pump")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_PUMP_BOOST_L, 0)
            elif button == "left" and  button_state == 2:
                log.debug("Requesting XPi Controls Manager Use main Left Pump")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_PUMP_BOOST_L, 2)
            elif button == "right" and  button_state == 0: 
                log.debug("Requesting XPi Controls Manager Use main Right Pump")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_PUMP_BOOST_R, 1)
            elif button == "right" and  button_state == 1:
                log.debug("Requesting XPi Controls Manager Don't use any Right Pump")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_PUMP_BOOST_R, 0)
            elif button == "right" and  button_state == 2:
                log.debug("Requesting XPi Controls Manager Use main Right Pump")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FUEL_PUMP_BOOST_R, 2)

            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.fornat_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.fornat_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
    
    def __flap_lever_moved(self, position) -> bool:
        log.debug("Enter")
        done = False

        try:
            if position == 0:
                log.debug("Requesting XPi Controls Manager Move Flaps to Up position")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FLAPS_LEVER, 0)
            elif  position == 1:
                log.debug("Requesting XPi Controls Manager Move Flaps to 1/4 position")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FLAPS_LEVER, 1/3)
            elif position == 2:
                log.debug("Requesting XPi Controls Manager Move Flaps to 1/2 position")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FLAPS_LEVER, 2/3)
            elif position == 3:
                log.debug("Requesting XPi Controls Manager Move Flaps to Down position")
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_FLAPS_LEVER, 1)
            done = True
        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.fornat_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.fornat_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
    
    def _trim_selector_button_toggle(self, button_state) -> bool:
        log.debug("Enter")
        done = False

        try:
            log.debug("Requesting XPi Controls Manager Toggle trim selector")
            if button_state == True:
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_AUTOPILOT_TRIM_SELECTOR, 1)
            else:
                self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_AUTOPILOT_TRIM_SELECTOR, 0)

        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.fornat_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.fornat_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)

    def _aux_trim_button_pressed(self, button_state) -> bool:
        log.debug("Enter")
        done = False

        try:
            log.debug("Requesting XPi Controls Manager Toggle aux trim selector")
            self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_AUX_TRIM_SELECTOR , button_state)

        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.format_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.format_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)

    def _engine_stop_feather_pressed(self, button_info) -> bool:
        log.debug("Enter")
        done = False

        try:
            log.debug("Requesting XPi Controls Manager change feather button")
            self.jg_ui_mngr_events_cb(JgXPiMngrEvents.JG_XPI_MNGR_EVENT_ENGINE_STOP_FEATHER , button_info)

        except ValueError as err:
            if(type(err.args[0]) is int):
                if (err.args[0] == 0):
                    # Leaving early successfully
                    done = True
                else:
                    # We failed, error already displayed
                    done = False
            else:
                # Actual ValueError err
                log.error("%s", traceback.format_exc())
                log.error("Exception: %s", err)
                done = False
        except Exception as err:
            log.error("%s", traceback.format_exc())
            log.error("Exception: %s", err)
            done = False

        log.debug("Exit")
        return(done)
# ----------------------------------------------------------------------------------

# DONE -----------------------------------------------------------------------------
        
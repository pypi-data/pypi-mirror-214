import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox

def showImage(matrix, inputted = 0, mainTitle='"No title"'):
    # Initialize phase type and magnitude
    phase_type = 'wrapped'
    left_image = 'magnitude'
    # unwrap phase
    ax_unwrap_level = None
    ax_unwrap_window = None
    slider_unwrap_level = None
    slider_unwrap_window = None
    # real
    ax_real_level = None
    ax_real_window = None
    slider_real_level = None
    slider_real_window = None
    # imaginary
    ax_imag_level = None
    ax_imag_window = None
    slider_imag_level = None
    slider_imag_window = None
    # Initialize Text Boxes
    y_text_box = None
    y_axbox = None
    x_text_box = None
    x_axbox = None
    ########################################################################################################################################
    if np.iscomplex(matrix).any() == True:
        # Initialize the figure
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plt.ion()
        plt.suptitle(mainTitle)
        # CHANGES THE BRIGHTNESS OF THE MATRIX
        # Initialize the magnitude and wrapped phase
        if inputted == 0:
            mag = np.abs(matrix)
            im1 = ax1.imshow(mag, cmap='gray', interpolation='nearest')
            phase = np.angle(matrix)
            im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
        else:
            for x in range(1,inputted+1):
                matrix *= 1.5
                mag = np.abs(matrix)
                im1 = ax1.imshow(mag, cmap='gray', interpolation='nearest')
                phase = np.angle(matrix)
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                fig.canvas.draw()
                fig.canvas.flush_events()
                print("changed")
                plt.pause(0.1)
        # Initialize the titles and colorbars
        ax1.set_title(f"{mainTitle} Magnitude")
        cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
        ax2.set_title(f"{mainTitle} Wrapped Phase")
        cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
        # Define the slider parameters
        mag_level_range = (np.min(mag), np.max(mag))
        mag_window_range = (0, np.max(mag) - np.min(mag))
        phase_level_range = (np.min(phase), np.max(phase))
        phase_window_range = (0, np.max(phase) - np.min(phase))
        # Create the sliders
        ax_mag_level = plt.axes([0.095, 0.05, 0.3, 0.03])
        ax_mag_window = plt.axes([0.095, 0.01, 0.3, 0.03])
        slider_mag_level = Slider(ax_mag_level, 'Level', *mag_level_range, valinit=(np.max(mag) + np.min(mag)) / 2)
        slider_mag_window = Slider(ax_mag_window, 'Window', *mag_window_range, valinit=np.max(mag) - np.min(mag))
        ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
        ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
        slider_phase_level = Slider(ax_phase_level, 'Level', *phase_level_range, valinit=(np.max(phase) + np.min(phase)) / 2)
        slider_phase_window = Slider(ax_phase_window, 'Window', *phase_window_range, valinit=np.max(phase) - np.min(phase))
        # Enable blitting for better performance
        fig.canvas.draw()
        background1 = fig.canvas.copy_from_bbox(ax1.bbox)
        background2 = fig.canvas.copy_from_bbox(ax2.bbox)
        # Update the magnitude and phase images with blitting
        def update_left_blit(val, im, level_slider, window_slider):
            fig.canvas.restore_region(background1)
            level = level_slider.val
            window = window_slider.val
            im.set_clim([level - window / 2, level + window / 2])
            ax1.draw_artist(im)
            fig.canvas.blit(ax1.bbox)
        def update_right_blit(val, im, level_slider, window_slider):
            fig.canvas.restore_region(background2)
            level = level_slider.val
            window = window_slider.val
            im.set_clim([level - window / 2, level + window / 2])
            ax2.draw_artist(im)
            fig.canvas.blit(ax2.bbox)
        # Connect the slider update functions with blitting
        slider_mag_level.on_changed(lambda val: update_left_blit(val, im1, slider_mag_level, slider_mag_window))
        slider_mag_window.on_changed(lambda val: update_left_blit(val, im1, slider_mag_level, slider_mag_window))
        slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
        slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
        ########################################################################################################################################
        phase_unwrapped = np.unwrap(phase)
        i0 = int(phase_unwrapped.shape[0] / 2)
        i1 = int(phase_unwrapped.shape[1] / 2)
        phase0 = phase_unwrapped[i0, i1]
        phase_unwrapped -= phase0
        ########################################################################################################################################
        # MAIN METHIDS STARTS HERE 
        ########################################################################################################################################
        def update_phase():
            nonlocal phase_type
            nonlocal cb2
            nonlocal y_text_box
            nonlocal y_axbox
            nonlocal x_text_box
            nonlocal x_axbox
            nonlocal ax_phase_level
            nonlocal ax_phase_window
            nonlocal slider_phase_level
            nonlocal slider_phase_window
            nonlocal ax_unwrap_level
            nonlocal ax_unwrap_window
            nonlocal slider_unwrap_level
            nonlocal slider_unwrap_window
            ########################################################################################################################################
            if phase_type == 'wrapped':
                if y_axbox:  # If axbox exists, remove it
                    y_axbox.remove()
                    y_axbox = None
                    y_text_box = None
                if x_axbox:
                    x_axbox.remove()
                    x_axbox = None
                    x_text_box = None
                if ax_unwrap_level:
                    ax_unwrap_level.remove()
                    ax_unwrap_level = None
                    slider_unwrap_level = None
                if ax_unwrap_window:
                    ax_unwrap_window.remove()
                    ax_unwrap_window = None
                    slider_unwrap_window = None
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                ax2.set_title(f"{mainTitle} Wrapped Phase")
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_phase_level = Slider(ax_phase_level, 'Level', np.min(phase), np.max(phase), valinit=(np.max(phase) + np.min(phase)) / 2)
                slider_phase_window = Slider(ax_phase_window, 'Window', np.min(phase), np.max(phase), valinit=np.max(phase) - np.min(phase))
                # slider listener
                slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
                slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
            ########################################################################################################################################
            else: #else when unwrapped
                if ax_phase_level:
                    ax_phase_level.remove()
                    ax_phase_level = None
                    slider_phase_level = None
                if ax_phase_window:
                    ax_phase_window.remove()
                    ax_phase_window = None
                    slider_phase_window = None
                im2 = ax2.imshow(phase_unwrapped, cmap='gray', interpolation='nearest')
                ax2.set_title(f"{mainTitle} Unwrapped Phase")
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                # Create Slider
                ax_unwrap_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                ax_unwrap_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_unwrap_level = Slider(ax_unwrap_level, 'Level', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=(np.max(phase_unwrapped) + np.min(phase_unwrapped)) / 2)
                slider_unwrap_window = Slider(ax_unwrap_window, 'Window', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=np.max(phase_unwrapped) - np.min(phase_unwrapped))
                #slider listener
                slider_unwrap_level.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
                slider_unwrap_window.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
                # Create textbox
                y_axbox = plt.axes([0.63, 0.90, 0.05, 0.04])
                y_text_box = TextBox(y_axbox, label='y-slice', initial='')
                x_axbox = plt.axes([0.82, 0.90, 0.05, 0.04])
                x_text_box = TextBox(x_axbox, label='x-slice', initial='')
                def sumbit_y_axis(text):
                    plot_y_slice(phase_unwrapped, text, mainTitle)
                def submit_x_axis(text):
                    plot_x_slice(phase_unwrapped, text, mainTitle)
                y_text_box.on_submit(sumbit_y_axis)
                x_text_box.on_submit(submit_x_axis)
        ########################################################################################################################################
        def update_images():
            nonlocal phase_type
            nonlocal left_image
            nonlocal cb1
            nonlocal cb2
            nonlocal y_text_box
            nonlocal y_axbox
            nonlocal x_text_box
            nonlocal x_axbox
            nonlocal switch_phase_button
            nonlocal phaseButton
            nonlocal switch_image_button
            nonlocal imageButton
            nonlocal ax_mag_level
            nonlocal ax_mag_window
            nonlocal slider_mag_level
            nonlocal slider_mag_window
            nonlocal ax_phase_level
            nonlocal ax_phase_window
            nonlocal slider_phase_level
            nonlocal slider_phase_window
            nonlocal ax_unwrap_level
            nonlocal ax_unwrap_window
            nonlocal slider_unwrap_level
            nonlocal slider_unwrap_window
            nonlocal ax_real_level
            nonlocal ax_real_window
            nonlocal slider_real_level
            nonlocal slider_real_window
            nonlocal ax_imag_level
            nonlocal ax_imag_window
            nonlocal slider_imag_level
            nonlocal slider_imag_window
            ########################################################################################################################################
            if left_image == 'real':
                if y_axbox:  # If axbox exists, remove it
                    y_axbox.remove()
                    y_axbox = None
                    y_text_box = None
                if x_axbox:
                    x_axbox.remove()
                    x_axbox = None
                    x_text_box = None
                if switch_phase_button:
                    switch_phase_button.remove()
                    switch_phase_button = None
                    phaseButton = None
                if ax_mag_level:
                    ax_mag_level.remove()
                    ax_mag_level = None 
                    slider_mag_level = None
                if ax_mag_window:
                    ax_mag_window.remove()
                    ax_mag_window = None 
                    slider_mag_window = None
                if ax_phase_level:
                    ax_phase_level.remove()
                    ax_phase_level = None
                    slider_phase_level = None
                if ax_phase_window:
                    ax_phase_window.remove()
                    ax_phase_window = None
                    slider_phase_window = None
                if ax_unwrap_level:
                    ax_unwrap_level.remove()
                    ax_unwrap_level = None
                    slider_unwrap_level = None
                if ax_unwrap_window:
                    ax_unwrap_window.remove()
                    ax_unwrap_window = None
                    slider_unwrap_window = None
                real = matrix.real
                imag = matrix.imag
                im1 = ax1.imshow(real, cmap='gray', interpolation='nearest')
                im2 = ax2.imshow(imag, cmap='gray', interpolation='nearest')
                ax1.set_title("Real")
                ax2.set_title("Imaginary")
                cb1.remove()
                cb2.remove()
                cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                # initialize and show slider
                ax_real_level = plt.axes([0.095, 0.05, 0.3, 0.03])
                ax_real_window = plt.axes([0.095, 0.01, 0.3, 0.03])
                slider_real_level = Slider(ax_real_level, 'Level', np.min(real), np.max(real), valinit=(np.max(real) + np.min(real)) / 2)
                slider_real_window = Slider(ax_real_window, 'Window', np.min(real), np.max(real), valinit=np.max(real) - np.min(real))
                ax_imag_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                ax_imag_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_imag_level = Slider(ax_imag_level, 'Level', np.min(imag), np.max(imag), valinit=(np.max(imag) + np.min(imag)) / 2)
                slider_imag_window = Slider(ax_imag_window, 'Window', np.min(imag), np.max(imag), valinit=np.max(imag) - np.min(imag))
                #slider listener
                slider_real_level.on_changed(lambda val: update_left_blit(val, im1, slider_real_level, slider_real_window))
                slider_real_window.on_changed(lambda val: update_left_blit(val, im1, slider_real_level, slider_real_window))
                slider_imag_level.on_changed(lambda val: update_right_blit(val, im2, slider_imag_level, slider_imag_window))
                slider_imag_window.on_changed(lambda val: update_right_blit(val, im2, slider_imag_level, slider_imag_window))
            ########################################################################################################################################
            else:
                if ax_real_level:
                    ax_real_level.remove()
                    ax_real_level = None
                    slider_real_level = None
                if ax_real_window:
                    ax_real_window.remove()
                    ax_real_window = None
                    slider_real_window = None
                if ax_imag_level:
                    ax_imag_level.remove()
                    ax_imag_level = None
                    slider_imag_level = None
                if ax_imag_window:
                    ax_imag_window.remove()
                    ax_imag_window = None
                    slider_imag_window = None
                # show image
                im1 = ax1.imshow(mag, cmap='gray', interpolation='nearest')
                ax1.set_title(f"{mainTitle} Magnitude")
                cb1.remove()
                cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
                # show image
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                ax2.set_title(f"{mainTitle} Wrapped Phase")
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                # initialize and show slider (mag)
                ax_mag_level = plt.axes([0.095, 0.05, 0.3, 0.03])
                ax_mag_window = plt.axes([0.095, 0.01, 0.3, 0.03])
                slider_mag_level = Slider(ax_mag_level, 'Level', np.min(mag), np.max(mag), valinit=(np.max(mag) + np.min(mag)) / 2)
                slider_mag_window = Slider(ax_mag_window, 'Window', np.min(mag), np.max(mag), valinit=np.max(mag) - np.min(mag))
                # initialize and show slider (phase)
                ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_phase_level = Slider(ax_phase_level, 'Level', np.min(phase), np.max(phase), valinit=(np.max(phase) + np.min(phase)) / 2)
                slider_phase_window = Slider(ax_phase_window, 'Window', np.min(phase), np.max(phase), valinit=np.max(phase) - np.min(phase))
                # Connect the slider update functions with blitting
                slider_mag_level.on_changed(lambda val: update_left_blit(val, im1, slider_mag_level, slider_mag_window))
                slider_mag_window.on_changed(lambda val: update_left_blit(val, im1, slider_mag_level, slider_mag_window))
                slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
                slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
                # button
                switch_phase_button = plt.axes([0.61, 0.96, 0.27, 0.04])
                phaseButton = Button(switch_phase_button, 'Wrapped<->Unwrapped')
                phaseButton.on_clicked(toggle_phase)
        ########################################################################################################################################
        def toggle_phase(event):
            nonlocal phase_type
            if phase_type == 'wrapped':
                phase_type = 'unwrapped'
            else:
                phase_type = 'wrapped'
            update_phase()
        ########################################################################################################################################
        def toggle_plot(event):
            nonlocal phase_type
            nonlocal left_image
            if left_image == 'magnitude':
                left_image = 'real'
                phase_type = 'wrapped'
            else:
                left_image = 'magnitude'
            update_images()
        ########################################################################################################################################
        # initial buttons
        switch_phase_button = plt.axes([0.61, 0.96, 0.27, 0.04])
        phaseButton = Button(switch_phase_button, 'Wrapped<->Unwrapped')
        switch_image_button = plt.axes([0.135, 0.96, 0.21, 0.04])
        imageButton = Button(switch_image_button, 'Mag<->Real/Imag')
        phaseButton.on_clicked(toggle_phase)
        imageButton.on_clicked(toggle_plot)
        ########################################################################################################################################
        # initialize reset button
        def reset(event):
            nonlocal im1
            nonlocal im2
            nonlocal cb1
            nonlocal cb2
            nonlocal ax_mag_level
            nonlocal slider_mag_level
            nonlocal ax_mag_window
            nonlocal slider_mag_window
            nonlocal ax_phase_level
            nonlocal slider_phase_level
            nonlocal ax_phase_window
            nonlocal slider_phase_window
            nonlocal ax_unwrap_level
            nonlocal slider_unwrap_level
            nonlocal ax_unwrap_window
            nonlocal slider_unwrap_window
            nonlocal ax_real_level
            nonlocal slider_real_level
            nonlocal ax_real_window
            nonlocal slider_real_window
            nonlocal ax_imag_level
            nonlocal slider_imag_level
            nonlocal ax_imag_window
            nonlocal slider_imag_window
            if ax_mag_level and ax_mag_window:
                im1 = ax1.imshow(mag, cmap='gray', interpolation='nearest')
                cb1.remove()
                cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
                ax_mag_level.remove()
                ax_mag_level = plt.axes([0.095, 0.05, 0.3, 0.03])
                slider_mag_level = Slider(ax_mag_level, 'Level', np.min(mag), np.max(mag), valinit=(np.max(mag) + np.min(mag)) / 2)
                ax_mag_window.remove()
                ax_mag_window = plt.axes([0.095, 0.01, 0.3, 0.03])
                slider_mag_window = Slider(ax_mag_window, 'Window', np.min(mag), np.max(mag), valinit=np.max(mag) - np.min(mag))
                slider_mag_level.on_changed(lambda val: update_left_blit(val, im1, slider_mag_level, slider_mag_window))
                slider_mag_window.on_changed(lambda val: update_left_blit(val, im1, slider_mag_level, slider_mag_window))
            if ax_phase_level and ax_phase_window:
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_phase_level.remove()
                ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                slider_phase_level = Slider(ax_phase_level, 'Level', np.min(phase), np.max(phase), valinit=(np.max(phase) + np.min(phase)) / 2)
                ax_phase_window.remove()
                ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_phase_window = Slider(ax_phase_window, 'Window', np.min(phase), np.max(phase), valinit=np.max(phase) - np.min(phase))
                slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
                slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
            if ax_unwrap_level and ax_unwrap_window:
                im2 = ax2.imshow(phase_unwrapped, cmap='gray', interpolation='nearest')
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_unwrap_level.remove()
                ax_unwrap_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                slider_unwrap_level = Slider(ax_unwrap_level, 'Level', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=(np.max(phase_unwrapped) + np.min(phase_unwrapped)) / 2)
                ax_unwrap_window.remove()
                ax_unwrap_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_unwrap_window = Slider(ax_unwrap_window, 'Window', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=np.max(phase_unwrapped) - np.min(phase_unwrapped))
                slider_unwrap_level.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
                slider_unwrap_window.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
            if ax_real_level and ax_real_window:
                real = matrix.real
                im1 = ax1.imshow(real, cmap='gray', interpolation='nearest')
                cb1.remove()
                cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
                ax_real_level.remove()
                ax_real_level = plt.axes([0.095, 0.05, 0.3, 0.03])
                slider_real_level = Slider(ax_real_level, 'Level', np.min(real), np.max(real), valinit=(np.max(real) + np.min(real)) / 2)
                ax_real_window.remove()
                ax_real_window = plt.axes([0.095, 0.01, 0.3, 0.03])
                slider_real_window = Slider(ax_real_window, 'Window', np.min(real), np.max(real), valinit=np.max(real) - np.min(real))
                slider_real_level.on_changed(lambda val: update_left_blit(val, im1, slider_real_level, slider_real_window))
                slider_real_window.on_changed(lambda val: update_left_blit(val, im1, slider_real_level, slider_real_window))
            if ax_imag_level and ax_imag_window:
                imag = matrix.imag
                im2 = ax2.imshow(imag, cmap='gray', interpolation='nearest')
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_imag_level.remove()
                ax_imag_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                slider_imag_level = Slider(ax_imag_level, 'Level', np.min(imag), np.max(imag), valinit=(np.max(imag) + np.min(imag)) / 2)
                ax_imag_window.remove()
                ax_imag_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_imag_window = Slider(ax_imag_window, 'Window', np.min(imag), np.max(imag), valinit=np.max(imag) - np.min(imag))
                slider_imag_level.on_changed(lambda val: update_right_blit(val, im2, slider_imag_level, slider_imag_window))
                slider_imag_window.on_changed(lambda val: update_right_blit(val, im2, slider_imag_level, slider_imag_window))
        reset_sliders = plt.axes([0.47, 0.87, 0.065, 0.04])
        resetButton = Button(reset_sliders, 'Reset')
        resetButton.on_clicked(reset)
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)
        plt.ioff()
        plt.show(block=False)
        return phaseButton, imageButton, resetButton, y_text_box, x_text_box, slider_mag_level, slider_mag_window, slider_phase_level, slider_phase_window, slider_unwrap_level, slider_unwrap_window, slider_real_level, slider_real_window, slider_imag_level, slider_imag_window

    ########################################################################################################################################
    ########################################################################################################################################
    ########################################################################################################################################
    ########################################################################################################################################

    elif np.isreal(matrix).all() == True:
        # Initialize the figure
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plt.ion()
        plt.suptitle(mainTitle)
        ########################################################################################################################################
        # CHANGES THE BRIGHTNESS OF THE MATRIX
        if inputted == 0:
            im1 = ax1.imshow(matrix, cmap='gray', interpolation='nearest')
            mfft = np.fft.fftshift(np.fft.fft2(matrix))
            phase = np.angle(mfft)
            im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
        else:
            for x in range(1,inputted+1):
                matrix *= 1.5
                im1 = ax1.imshow(matrix, cmap='gray', interpolation='nearest')
                mfft = np.fft.fftshift(np.fft.fft2(matrix))
                phase = np.angle(mfft)
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                fig.canvas.draw()
                fig.canvas.flush_events()
                print("changed")
                plt.pause(0.1)
        ax1.set_title(f"{mainTitle} Real")
        cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
        ax2.set_title(f"{mainTitle} Wrapped Phase")
        cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
        ax_raw_level = plt.axes([0.095, 0.05, 0.3, 0.03])
        ax_raw_window = plt.axes([0.095, 0.01, 0.3, 0.03])
        slider_raw_level = Slider(ax_raw_level, 'Level', np.min(matrix), np.max(matrix), valinit=(np.max(matrix) + np.min(matrix)) / 2)
        slider_raw_window = Slider(ax_raw_window, 'Window', np.min(matrix), np.max(matrix), valinit=np.max(matrix) - np.min(matrix))
        ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
        ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
        slider_phase_level = Slider(ax_phase_level, 'Level', np.min(phase), np.max(phase), valinit=(np.max(phase) + np.min(phase)) / 2)
        slider_phase_window = Slider(ax_phase_window, 'Window', np.min(phase), np.max(phase), valinit=np.max(phase) - np.min(phase))
        # Enable blitting for better performance
        fig.canvas.draw()
        background1 = fig.canvas.copy_from_bbox(ax1.bbox)
        background2 = fig.canvas.copy_from_bbox(ax2.bbox)
        # Update the magnitude and phase images with blitting
        def update_left_blit(val, im, level_slider, window_slider):
            fig.canvas.restore_region(background1)
            level = level_slider.val
            window = window_slider.val
            im.set_clim([level - window / 2, level + window / 2])
            ax1.draw_artist(im)
            fig.canvas.blit(ax1.bbox)
        def update_right_blit(val, im, level_slider, window_slider):
            fig.canvas.restore_region(background2)
            level = level_slider.val
            window = window_slider.val
            im.set_clim([level - window / 2, level + window / 2])
            ax2.draw_artist(im)
            fig.canvas.blit(ax2.bbox)
        # Connect the slider update functions with blitting
        slider_raw_level.on_changed(lambda val: update_left_blit(val, im1, slider_raw_level, slider_raw_window))
        slider_raw_window.on_changed(lambda val: update_left_blit(val, im1, slider_raw_level, slider_raw_window))
        slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
        slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
        ########################################################################################################################################
        phase_unwrapped = np.unwrap(phase)
        i0 = int(phase_unwrapped.shape[0] / 2)
        i1 = int(phase_unwrapped.shape[1] / 2)
        phase0 = phase_unwrapped[i0, i1]
        phase_unwrapped -= phase0
        ########################################################################################################################################
        # method to update the phase
        def update_phase():
            nonlocal phase_type
            nonlocal cb2
            nonlocal y_text_box
            nonlocal y_axbox
            nonlocal x_text_box
            nonlocal x_axbox
            nonlocal ax_phase_level
            nonlocal ax_phase_window
            nonlocal slider_phase_level
            nonlocal slider_phase_window
            nonlocal ax_unwrap_level
            nonlocal ax_unwrap_window
            nonlocal slider_unwrap_level
            nonlocal slider_unwrap_window
            ########################################################################################################################################
            if phase_type == 'wrapped':
                if y_axbox:  # If axbox exists, remove it
                    y_axbox.remove()
                    y_axbox = None
                    y_text_box = None
                if x_axbox:
                    x_axbox.remove()
                    x_axbox = None
                    x_text_box = None
                if ax_unwrap_level:
                    ax_unwrap_level.remove()
                    ax_unwrap_level = None
                    slider_unwrap_level = None
                if ax_unwrap_window:
                    ax_unwrap_window.remove()
                    ax_unwrap_window = None
                    slider_unwrap_window = None
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                ax2.set_title(f"{mainTitle} Wrapped Phase")
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_phase_level = Slider(ax_phase_level, 'Level', np.min(phase), np.max(phase), valinit=(np.max(phase) + np.min(phase)) / 2)
                slider_phase_window = Slider(ax_phase_window, 'Window', np.min(phase), np.max(phase), valinit=np.max(phase) - np.min(phase))
                # slider listener
                slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
                slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
            ########################################################################################################################################
            else:
                if ax_phase_level:
                    ax_phase_level.remove()
                    ax_phase_level = None
                    slider_phase_level = None
                if ax_phase_window:
                    ax_phase_window.remove()
                    ax_phase_window = None
                    slider_phase_window = None
                im2 = ax2.imshow(phase_unwrapped, cmap='gray', interpolation='nearest')
                ax2.set_title(f"{mainTitle} Unwrapped Phase")
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                # Create Slider
                ax_unwrap_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                ax_unwrap_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_unwrap_level = Slider(ax_unwrap_level, 'Level', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=(np.max(phase_unwrapped) + np.min(phase_unwrapped)) / 2)
                slider_unwrap_window = Slider(ax_unwrap_window, 'Window', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=np.max(phase_unwrapped) - np.min(phase_unwrapped))
                #slider listener
                slider_unwrap_level.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
                slider_unwrap_window.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
                # Create textbox
                y_axbox = plt.axes([0.63, 0.90, 0.05, 0.04])
                y_text_box = TextBox(y_axbox, label='y-slice', initial='')
                x_axbox = plt.axes([0.82, 0.90, 0.05, 0.04])
                x_text_box = TextBox(x_axbox, label='x-slice', initial='')
                def sumbit_y_axis(text):
                    plot_y_slice(phase_unwrapped, text, mainTitle)
                def submit_x_axis(text):
                    plot_x_slice(phase_unwrapped, text, mainTitle)
                y_text_box.on_submit(sumbit_y_axis)
                x_text_box.on_submit(submit_x_axis)
        ########################################################################################################################################
        def toggle_phase(event):
            nonlocal phase_type
            if phase_type == 'wrapped':
                phase_type = 'unwrapped'
            else:
                phase_type = 'wrapped'
            update_phase()
        switch_phase_button = plt.axes([0.61, 0.96, 0.27, 0.04])
        phaseButton = Button(switch_phase_button, 'Wrapped<->Unwrapped')
        phaseButton.on_clicked(toggle_phase)
        ########################################################################################################################################
        def reset(event):
            nonlocal im1
            nonlocal im2
            nonlocal cb1
            nonlocal cb2
            nonlocal ax_raw_level
            nonlocal slider_raw_level
            nonlocal ax_raw_window
            nonlocal slider_raw_window
            nonlocal ax_phase_level
            nonlocal slider_phase_level
            nonlocal ax_phase_window
            nonlocal slider_phase_window
            nonlocal ax_unwrap_level
            nonlocal slider_unwrap_level
            nonlocal ax_unwrap_window
            nonlocal slider_unwrap_window
            if ax_raw_level and ax_raw_window:
                im1 = ax1.imshow(matrix, cmap='gray', interpolation='nearest')
                cb1.remove()
                cb1 = plt.colorbar(im1, ax=ax1, shrink=0.4)
                ax_raw_level.remove()
                ax_raw_level = plt.axes([0.095, 0.05, 0.3, 0.03])
                slider_raw_level = Slider(ax_raw_level, 'Level', np.min(matrix), np.max(matrix), valinit=(np.max(matrix) + np.min(matrix)) / 2)
                ax_raw_window.remove()
                ax_raw_window = plt.axes([0.095, 0.01, 0.3, 0.03])
                slider_raw_window = Slider(ax_raw_window, 'Window', np.min(matrix), np.max(matrix), valinit=np.max(matrix) - np.min(matrix))
                slider_raw_level.on_changed(lambda val: update_left_blit(val, im1, slider_raw_level, slider_raw_window))
                slider_raw_window.on_changed(lambda val: update_left_blit(val, im1, slider_raw_level, slider_raw_window))
            if ax_phase_level and ax_phase_window:
                im2 = ax2.imshow(phase, cmap='gray', interpolation='nearest')
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_phase_level.remove()
                ax_phase_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                slider_phase_level = Slider(ax_phase_level, 'Level', np.min(phase), np.max(phase), valinit=(np.max(phase) + np.min(phase)) / 2)
                ax_phase_window.remove()
                ax_phase_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_phase_window = Slider(ax_phase_window, 'Window', np.min(phase), np.max(phase), valinit=np.max(phase) - np.min(phase))
                slider_phase_level.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
                slider_phase_window.on_changed(lambda val: update_right_blit(val, im2, slider_phase_level, slider_phase_window))
            if ax_unwrap_level and ax_unwrap_window:
                im2 = ax2.imshow(phase_unwrapped, cmap='gray', interpolation='nearest')
                cb2.remove()
                cb2 = plt.colorbar(im2, ax=ax2, shrink=0.4)
                ax_unwrap_level.remove()
                ax_unwrap_level = plt.axes([0.61, 0.05, 0.3, 0.03])
                slider_unwrap_level = Slider(ax_unwrap_level, 'Level', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=(np.max(phase_unwrapped) + np.min(phase_unwrapped)) / 2)
                ax_unwrap_window.remove()
                ax_unwrap_window = plt.axes([0.61, 0.01, 0.3, 0.03])
                slider_unwrap_window = Slider(ax_unwrap_window, 'Window', np.min(phase_unwrapped), np.max(phase_unwrapped), valinit=np.max(phase_unwrapped) - np.min(phase_unwrapped))
                slider_unwrap_level.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
                slider_unwrap_window.on_changed(lambda val: update_right_blit(val, im2, slider_unwrap_level, slider_unwrap_window))
        ########################################################################################################################################
        reset_sliders = plt.axes([0.47, 0.87, 0.065, 0.04])
        resetButton = Button(reset_sliders, 'Reset')
        resetButton.on_clicked(reset)
        fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)
        plt.ioff()
        plt.show(block=False)
        return phaseButton, resetButton, y_text_box, x_text_box, slider_raw_level, slider_raw_window, slider_phase_level, slider_phase_window, slider_unwrap_level, slider_unwrap_window
    
def plot_y_slice(phase_unwrapped, y, title):
    # Plot the y-axis slice, returns a tuple
    fig, ax = plt.subplots()
    ax.plot(phase_unwrapped[int(y), :])
    ax.set_title(f"{title} (y = {y})")
    plt.show(block=False)

def plot_x_slice(phase_unwrapped, x, title):
    # Plot the y-axis slice, using tuple
    fig, ax = plt.subplots()
    ax.plot(phase_unwrapped[:, int(x)])
    ax.set_title(f"{title} (x = {x})")
    plt.show(block=False)

def showPairs(matrix, mainTitle, unwrapPhase=0):
    fig = plt.figure()

    # shows the image only
    fig.add_subplot(1, 3, 1)
    plt.suptitle(mainTitle)
    plt.imshow(matrix, cmap='gray', interpolation='nearest')
    plt.title(f"{mainTitle} Image")
    # Calculate (height_of_image / width_of_image)
    image_ratio1 = matrix.shape[0]/matrix.shape[1]
    # Plot vertical colorbar
    plt.colorbar(fraction=0.045*image_ratio1)

    # shows the fourier transform
    fig.add_subplot(1, 3, 2)
    mfft = np.fft.fftshift(np.fft.fft2(matrix))
    plt.imshow(np.log(abs(mfft)), cmap='gray', interpolation='nearest')
    plt.title(f"{mainTitle} Fourier Log Mag")
    # Calculate (height_of_image / width_of_image)
    image_ratio2 = np.log(abs(mfft)).shape[0]/np.log(abs(mfft)).shape[1]
    # Plot vertical colorbar
    plt.colorbar(fraction=0.045*image_ratio2)

    # shows the phase of fourier transform
    fig.add_subplot(1, 3, 3)
    #phase = np.angle(mfft)
    if unwrapPhase != 0:
        phase = np.unwrap(np.angle(mfft))
        # use phase at zero frquency as 0
        i0 = int(phase.shape[0] / 2)
        i1 = int(phase.shape[1] / 2)
        phase0 = phase[i0, i1]
        phase -= phase0
        plt.imshow(phase, cmap='gray', interpolation='nearest')
        plt.title(f"{mainTitle} Unwrapped Phase")
    else:
        phase = np.angle(mfft)
        plt.imshow(phase, cmap='gray', interpolation='nearest')
        plt.title(f"{mainTitle} Wrapped Phase")
    # Calculate (height_of_image / width_of_image)
    image_ratio3 = phase.shape[0]/phase.shape[1]
    # Plot vertical colorbar
    plt.colorbar(fraction=0.045*image_ratio3)
    fig.tight_layout()
    plt.show(block=False)

def showPlot(m, mainTitle='"No title"'):
    if np.isreal(m).all() == True:
        real = m.real
        fig = plt.figure()
        plt.imshow(real, cmap='gray', interpolation='nearest')
        plt.title("Real")
        plt.colorbar()
        fig.tight_layout()
        plt.show(block=False)
    else:
        real = m.real
        imag = m.imag
        # creates a figure
        fig = plt.figure()
        plt.suptitle(mainTitle)
        # add a grid 1x2 in the 2nd subplot position
        fig.add_subplot(1, 2, 1)
        plt.imshow(real, cmap='gray', interpolation='nearest')
        plt.title("Real")
        plt.colorbar(shrink=0.5)
        fig.add_subplot(1, 2, 2)
        plt.imshow(imag, cmap='gray', interpolation='nearest')
        plt.title("Imaginary")
        plt.colorbar(shrink=0.5)
        fig.tight_layout()
        plt.show(block=False)
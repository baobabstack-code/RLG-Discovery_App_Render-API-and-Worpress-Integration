jQuery(document).ready(function ($) {
    // Tab switching functionality
    $('.rlg-tab').on('click', function () {
        var $this = $(this);
        var tabId = $this.data('tab');
        var $container = $this.closest('.rlg-discovery-tabs-container');

        // Update active tab button
        $container.find('.rlg-tab').removeClass('active');
        $this.addClass('active');

        // Update active pane
        $container.find('.rlg-tab-pane').removeClass('active');
        $container.find('#rlg-pane-' + tabId).addClass('active');
    });

    // Form submission handler
    $('.rlg-discovery-form').on('submit', function (e) {
        e.preventDefault();

        var $form = $(this);
        var $status = $form.find('.rlg-status');
        var $btn = $form.find('button[type="submit"]');

        var endpoint = $form.data('endpoint');
        var apiUrl = rlgSettings.apiUrl + endpoint;

        var formData = new FormData(this);

        $status.html('Processing... <div class="rlg-spinner"></div>');
        $btn.prop('disabled', true);

        fetch(apiUrl, {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok: ' + response.statusText);
                }
                return response.blob();
            })
            .then(blob => {
                // Create download link
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;

                // Determine filename based on endpoint
                var filename = 'download.zip';
                if (endpoint === '/unlock') filename = 'unlocked_pdfs.zip';
                if (endpoint === '/organize') filename = 'organized_by_year.zip';
                if (endpoint === '/bates') filename = 'bates_labeled.zip';
                if (endpoint === '/redact') filename = 'redacted_output.zip';
                if (endpoint === '/index') filename = 'discovery_index.xlsx';

                a.download = filename;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);

                $status.html('<span style="color:green;">Success! Download started.</span>');
                $btn.prop('disabled', false);
            })
            .catch(error => {
                console.error('Error:', error);
                $status.html('<div style="color:red; background:#ffebeb; padding:10px; border:1px solid red; border-radius:4px;">' +
                    '<strong>Error:</strong> ' + error.message + '<br>' +
                    '<small>Attempted to connect to: ' + apiUrl + '</small><br>' +
                    '<small>Check console (F12) for details.</small>' +
                    '</div>');
                $btn.prop('disabled', false);
            });
    });
});

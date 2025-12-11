<?php
/**
 * Plugin Name: RLG Discovery Integration
 * Description: Integrates RLG Discovery Tools (Unlock, Organize, Bates, Redact) via shortcodes.
 * Version: 1.0.0
 * Author: RLG
 */

if (!defined('ABSPATH')) {
    exit;
}

// Define constants
define('RLG_DISCOVERY_PATH', plugin_dir_path(__FILE__));
define('RLG_DISCOVERY_URL', plugin_dir_url(__FILE__));

// Include Admin Settings
require_once RLG_DISCOVERY_PATH . 'admin/settings-page.php';

// Include Shortcodes
require_once RLG_DISCOVERY_PATH . 'public/shortcodes.php';

// Enqueue Scripts & Styles
function rlg_discovery_enqueue_scripts() {
    wp_enqueue_style('rlg-discovery-style', RLG_DISCOVERY_URL . 'public/css/style.css', array(), '1.0.0');
    
    wp_enqueue_script('rlg-discovery-client', RLG_DISCOVERY_URL . 'public/js/api-client.js', array('jquery'), '1.0.0', true);
    
    // Pass API URL to JS
    $api_url = get_option('rlg_discovery_api_url', 'https://discovery-api-b4c9.onrender.com');
    wp_localize_script('rlg-discovery-client', 'rlgSettings', array(
        'apiUrl' => rtrim($api_url, '/')
    ));
}
add_action('wp_enqueue_scripts', 'rlg_discovery_enqueue_scripts');

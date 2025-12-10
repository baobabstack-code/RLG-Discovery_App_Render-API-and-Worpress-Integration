<?php
if (!defined('ABSPATH')) {
    exit;
}

function rlg_shortcode_unlock($atts) {
    ob_start();
    ?>
    <div class="rlg-discovery-tool" id="rlg-unlock-tool">
        <h3>Unlock PDFs</h3>
        <form class="rlg-discovery-form" data-endpoint="/unlock" data-response-type="blob">
            <div class="rlg-form-group">
                <label>Upload PDFs or ZIP</label>
                <input type="file" name="files" multiple required accept=".pdf,.zip">
            </div>
            <div class="rlg-form-group">
                <label>Password Mode</label>
                <select name="password_mode">
                    <option value="Single password for all">Single password for all</option>
                    <option value="Try no password (for unencrypted files)">Try no password</option>
                </select>
            </div>
            <div class="rlg-form-group">
                <label>Password (if single)</label>
                <input type="password" name="password_for_all">
            </div>
            <button type="submit" class="rlg-btn">Unlock Files</button>
            <div class="rlg-status"></div>
        </form>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('rlg_unlock', 'rlg_shortcode_unlock');

function rlg_shortcode_organize($atts) {
    ob_start();
    ?>
    <div class="rlg-discovery-tool" id="rlg-organize-tool">
        <h3>Organize by Year</h3>
        <form class="rlg-discovery-form" data-endpoint="/organize" data-response-type="blob">
            <div class="rlg-form-group">
                <label>Upload PDFs or ZIP</label>
                <input type="file" name="files" multiple required accept=".pdf,.zip">
            </div>
            <div class="rlg-form-group">
                <label>Min Year</label>
                <input type="number" name="min_year" value="1900">
            </div>
            <div class="rlg-form-group">
                <label>Max Year</label>
                <input type="number" name="max_year" value="2099">
            </div>
            <button type="submit" class="rlg-btn">Organize Files</button>
            <div class="rlg-status"></div>
        </form>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('rlg_organize', 'rlg_shortcode_organize');

function rlg_shortcode_bates($atts) {
    ob_start();
    ?>
    <div class="rlg-discovery-tool" id="rlg-bates-tool">
        <h3>Bates Labeler</h3>
        <form class="rlg-discovery-form" data-endpoint="/bates" data-response-type="blob">
            <div class="rlg-form-group">
                <label>Upload PDFs or ZIP</label>
                <input type="file" name="files" multiple required accept=".pdf,.zip,.jpg,.png">
            </div>
            <div class="rlg-form-group">
                <label>Prefix</label>
                <input type="text" name="prefix" value="J.DOE">
            </div>
            <div class="rlg-form-group">
                <label>Start Number</label>
                <input type="number" name="start_num" value="1">
            </div>
            <div class="rlg-form-group">
                <label>Digits</label>
                <input type="number" name="digits" value="8">
            </div>
            <div class="rlg-form-group">
                <label>Zone</label>
                <select name="zone">
                    <option value="Bottom Right (Z3)">Bottom Right</option>
                    <option value="Bottom Center (Z2)">Bottom Center</option>
                    <option value="Bottom Left (Z1)">Bottom Left</option>
                </select>
            </div>
            <button type="submit" class="rlg-btn">Label Files</button>
            <div class="rlg-status"></div>
        </form>
    </div>
    <?php
    return ob_get_clean();
}
add_shortcode('rlg_bates', 'rlg_shortcode_bates');
